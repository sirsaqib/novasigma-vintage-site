// Vercel serverless function: publishes admin edits to the GitHub repo.
// POST /api/publish  { password, files: { "path": "content" }, message? }
// Env: GITHUB_TOKEN (fine-grained PAT, contents write), ADMIN_PASSWORD, GH_REPO (owner/repo)

export default async function handler(req, res) {
  if (req.method !== "POST") return res.status(405).json({ ok: false, error: "POST only" });

  let body = req.body;
  if (typeof body === "string") { try { body = JSON.parse(body); } catch { body = {}; } }

  if (!body || body.password !== process.env.ADMIN_PASSWORD) {
    return res.status(401).json({ ok: false, error: "Wrong password" });
  }
  const files = body.files || {};
  const paths = Object.keys(files).filter(p => /^[a-zA-Z0-9_\-./]+$/.test(p) && !p.includes("..") && p.length < 200);
  if (!paths.length) return res.status(400).json({ ok: false, error: "No files" });

  const repo = process.env.GH_REPO || "sirsaqib/novasigma-vintage-site";
  const token = process.env.GITHUB_TOKEN;
  if (!token) return res.status(500).json({ ok: false, error: "Server not configured" });

  const H = { "Authorization": `Bearer ${token}`, "Accept": "application/vnd.github+json", "Content-Type": "application/json" };
  const out = [];

  for (const p of paths) {
    const content = files[p];
    if (typeof content !== "string" || content.length > 4_000_000) {
      out.push({ path: p, ok: false, error: "bad content" }); continue;
    }
    try {
      // get current sha (if file exists)
      let sha = null;
      const g = await fetch(`https://api.github.com/repos/${repo}/contents/${encodeURIComponent(p)}`, { headers: H });
      if (g.ok) { const j = await g.json(); sha = j.sha; }

      const isImage = /\.(png|jpe?g|webp|gif)$/i.test(p);
      const payload = {
        message: body.message || `Admin update: ${p}`,
        content: isImage ? content : Buffer.from(content, "utf8").toString("base64"),
        ...(sha ? { sha } : {}),
      };
      const put = await fetch(`https://api.github.com/repos/${repo}/contents/${encodeURIComponent(p)}`, {
        method: "PUT", headers: H, body: JSON.stringify(payload),
      });
      const pj = await put.json();
      out.push({ path: p, ok: put.ok, sha: pj?.content?.sha?.slice(0, 7) || null, error: put.ok ? null : (pj.message || "github error") });
    } catch (e) {
      out.push({ path: p, ok: false, error: String(e).slice(0, 120) });
    }
  }

  const failed = out.filter(r => !r.ok);
  res.status(failed.length ? 207 : 200).json({ ok: !failed.length, results: out });
}
