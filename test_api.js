async function test() {
  console.log("--- STARTING FUNCTIONAL TEST ---");
  
  // Happy Path
  try {
    const res = await fetch("http://localhost:3000/api/documents/ingest", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        externalId: "doc-happy-001",
        patientId: "pt-12345",
        content: "Bệnh nhân Nguyễn Văn A, SĐT 0901234567 nhập viện.",
        type: "DISCHARGE"
      })
    });
    const data = await res.json();
    console.log("[HAPPY PATH] POST /api/documents/ingest:");
    console.log(`Status: ${res.status}`);
    console.log(data);
  } catch(e) { console.error(e) }

  // Status API Check (Happy Path part 2)
  try {
    const res = await fetch("http://localhost:3000/api/documents/doc-happy-001/status");
    const data = await res.json();
    console.log("\n[HAPPY PATH] GET /api/documents/doc-happy-001/status:");
    console.log(`Status: ${res.status}`);
    console.log(data);
  } catch(e) { console.error(e) }

  // Error Path
  try {
    const res = await fetch("http://localhost:3000/api/documents/ingest", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        externalId: "doc-error-002"
        // missing patientId, content, type
      })
    });
    const data = await res.json();
    console.log("\n[ERROR PATH] POST /api/documents/ingest (Missing fields):");
    console.log(`Status: ${res.status}`);
    console.log(data);
  } catch(e) { console.error(e) }

  console.log("--- TEST COMPLETED ---");
}

test();
