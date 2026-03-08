export async function injectSeoTags(html: string, path: string): Promise<string> {
  try {
    const response = await fetch(`http://localhost:8000/api/seo?path=${path}`);
    if (response.ok) {
      const seoData = await response.json() as {head_tags?: string};
      let newHtml = html;
      if (seoData.head_tags) {
        newHtml = newHtml.replace('<!-- __SEO_TAGS__ -->', seoData.head_tags);
      }
      return newHtml;
    }
  } catch (e) {
    console.error("Could not fetch SEO data from backend. Is it running?", e);
  }
  return html;
}
