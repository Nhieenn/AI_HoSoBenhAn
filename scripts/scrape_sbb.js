const fs = require('fs').promises;
const fsSync = require('fs');
const path = require('path');
const cheerio = require('cheerio');

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
  console.log('Đang thu thập danh sách link từ SBB...');
  
  const alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'.split('');
  const links = [];

  // Lặp qua các trang A-Z để lấy link
  for (const letter of alphabet) {
      const listUrl = `https://sbb.vn/ket-qua-tra-cuu?pid=${letter}`;
      const html = await fetchHtml(listUrl);
      if (!html) continue;

      const $ = cheerio.load(html);
      
      $('a').each((i, el) => {
          const href = $(el).attr('href');
          const title = $(el).text().trim();
          
          if (href && href.startsWith('https://sbb.vn/thu_vien_benh/') && title.length > 2) {
              if (!links.some(l => l.url === href)) {
                  links.push({ title, url: href });
              }
          }
      });
      await delay(200); // Tránh bị block
  }

  console.log(`Đã tìm thấy ${links.length} bài viết tiềm năng từ SBB.`);

  // Đọc file KB hiện tại
  let kb = [];
  try {
      if (fsSync.existsSync(KB_FILE_PATH)) {
          kb = JSON.parse(await fs.readFile(KB_FILE_PATH, 'utf8'));
      }
  } catch (e) {
      console.log('KB file chưa hợp lệ, tạo mới mảng rỗng.');
  }

  const existingSources = new Set(kb.map(k => k.metadata && k.metadata.sourceUrl).filter(Boolean));

  let addedCount = 0;
  const CONCURRENCY = 15;
  for (let i = 0; i < links.length; i += CONCURRENCY) {
      const chunk = links.slice(i, i + CONCURRENCY);
      
      await Promise.all(chunk.map(async (link) => {
          if (existingSources.has(link.url)) return;

          const articleHtml = await fetchHtml(link.url);
          if (!articleHtml) return;

          const $a = cheerio.load(articleHtml);
          const metaDesc = $a('meta[property="og:description"]').attr('content') || $a('meta[name="description"]').attr('content');
          
          if (metaDesc && metaDesc.length > 30) {
              // Nội dung bệnh từ SBB
              const finalContent = `${link.title}: ${metaDesc.trim().replace(/\\n/g, ' ')}`;
              
              kb.push({
                  content: finalContent,
                  metadata: {
                      source: 'SBB',
                      sourceUrl: link.url,
                      title: link.title
                  }
              });
              existingSources.add(link.url);
              addedCount++;
              console.log(`Đã thêm SBB: ${link.title}`);
          }
      }));

      await delay(500);
      await fs.writeFile(KB_FILE_PATH, JSON.stringify(kb, null, 2), 'utf8');
      
      if ((i + CONCURRENCY) % 30 === 0 || i + CONCURRENCY >= links.length) {
          console.log(`=> Tiến độ SBB: ${Math.min(i + CONCURRENCY, links.length)} / ${links.length}. Tổng số mới: ${addedCount}`);
      }
  }

  console.log(`Hoàn thành! Đã cào và lưu tổng cộng ${addedCount} bệnh mới từ SBB.`);
}

scrapeAll().catch(console.error);
