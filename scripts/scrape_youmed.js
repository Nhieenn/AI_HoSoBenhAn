const fs = require('fs').promises;
const fsSync = require('fs');
const path = require('path');
const cheerio = require('cheerio');

const BASE_URL = 'https://youmed.vn/tin-tuc/trieu-chung-benh/';
const KB_FILE_PATH = path.join(__dirname, '../knowledge_base.json');

const delay = ms => new Promise(res => setTimeout(res, ms));

async function fetchHtml(url, retries = 3) {
    for (let i = 0; i < retries; i++) {
        try {
            const res = await fetch(url);
            if (!res.ok) throw new Error(`HTTP ${res.status}`);
            return await res.text();
        } catch (e) {
            if (i === retries - 1) return null;
            await delay(1000);
        }
    }
}

async function scrapeAll() {
  console.log('Đang tải danh sách bệnh từ YouMed...');
  const html = await fetchHtml(BASE_URL);
  if (!html) {
      console.error('Không thể tải trang chủ!');
      return;
  }
  const $ = cheerio.load(html);
  
  const excluded = ['/tin-tuc/?s', '/duoc/', '/y-hoc-co-truyen/', '/kinh-nghiem-di-kham/', '/nuoi-day-con/', '/mang-thai/', '/hieu-ve-co-the-ban/', '/rang-ham-mat/', '/tai-mui-hong/', '/da-lieu/', '/nhan-khoa/', '/co-xuong-khop/', '/bi-quyet-song-khoe/', '/dinh-duong/', '/suc-khoe-nam-gioi/', '/suc-khoe-nu-gioi/', '/suc-khoe-tinh-duc/', '/than-kinh/', '/tim-mach/', '/ho-hap/', '/di-ung/', '/noi-tiet/', '/tieu-hoa/', '/than-tiet-nieu/', '/ung-buou/', '/xet-nghiem/', '/the-duc-the-thao/', '/tin-tuc/benh-vien', '/phong-kham', '/bac-si'];

  const links = [];
  $('a').each((i, el) => {
    const href = $(el).attr('href');
    const title = $(el).text().trim();
    if (href && href.startsWith('https://youmed.vn/tin-tuc/')) {
        let isExcluded = excluded.some(ex => href.includes(ex)) || href === 'https://youmed.vn/tin-tuc/' || title.toLowerCase() === 'trang chủ' || title.toLowerCase() === 'open search';
        if (!isExcluded && title.length > 2) {
            if (!links.some(l => l.url === href)) {
                links.push({ title, url: href });
            }
        }
    }
  });

  console.log(`Đã tìm thấy ${links.length} bài viết tiềm năng. Sẽ bắt đầu cào và lưu vào D:\\AI_HoSoBenhAn\\knowledge_base.json...`);

  let kb = [];
  try {
      if (fsSync.existsSync(KB_FILE_PATH)) {
          kb = JSON.parse(await fs.readFile(KB_FILE_PATH, 'utf8'));
      }
  } catch (e) {
      console.log('KB file chưa hợp lệ, tạo mới mảng rỗng.');
  }

  // Tracking existing
  const existingSources = new Set(kb.map(k => k.metadata.sourceUrl).filter(Boolean));
  // Add manual ones based on title matching so we don't duplicate early manual entries
  kb.forEach(k => {
      if (k.content) {
          const t = k.content.split(':')[0];
          existingSources.add(t);
      }
  });

  let addedCount = 0;
  const CONCURRENCY = 15; // Tăng nhẹ để nhanh hơn
  for (let i = 0; i < links.length; i += CONCURRENCY) {
      const chunk = links.slice(i, i + CONCURRENCY);
      
      await Promise.all(chunk.map(async (link) => {
          if (existingSources.has(link.url) || existingSources.has(link.title)) return;

          const articleHtml = await fetchHtml(link.url);
          if (!articleHtml) return;

          const $a = cheerio.load(articleHtml);
          
          let contentStr = '';
          const metaDesc = $a('meta[property="og:description"]').attr('content') || $a('meta[name="description"]').attr('content');
          
          let symptomsText = '';
          $a('h2, h3').each((idx, el) => {
              const text = $a(el).text().toLowerCase();
              if (text.includes('triệu chứng') || text.includes('dấu hiệu')) {
                  let nextEl = $a(el).next();
                  let localText = '';
                  let count = 0;
                  while (nextEl.length && count < 3 && !['H2', 'H3'].includes(nextEl[0].tagName)) {
                      localText += ' ' + nextEl.text().replace(/\\s+/g, ' ').trim();
                      nextEl = nextEl.next();
                      count++;
                  }
                  if (localText.length > 20) {
                      symptomsText = localText.trim();
                  }
              }
          });

          if (metaDesc || symptomsText) {
              const finalContent = `${link.title}: ${metaDesc ? metaDesc : ''} ${symptomsText ? 'Triệu chứng: ' + symptomsText : ''}`.trim();
              
              if (finalContent.length > 20) {
                  kb.push({
                      content: finalContent,
                      metadata: {
                          source: 'YouMed',
                          sourceUrl: link.url,
                          title: link.title
                      }
                  });
                  existingSources.add(link.url);
                  addedCount++;
                  console.log(`Đã thêm: ${link.title}`);
              }
          }
      }));

      await delay(500);
      await fs.writeFile(KB_FILE_PATH, JSON.stringify(kb, null, 2), 'utf8');
      
      if ((i + CONCURRENCY) % 30 === 0 || i + CONCURRENCY >= links.length) {
          console.log(`=> Tiến độ: ${Math.min(i + CONCURRENCY, links.length)} / ${links.length}. Tổng số bệnh mới: ${addedCount}`);
      }
  }

  console.log(`Hoàn thành! Đã cào và lưu tổng cộng ${addedCount} bệnh mới.`);
}

scrapeAll().catch(console.error);
