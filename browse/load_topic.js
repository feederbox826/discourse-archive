// external element for cloning
const externalLink = document.createElement('a');
externalLink.target = '_blank';
externalLink.rel = 'noopener noreferrer';
externalLink.className = 'external';

const mainEl = document.getElementById('main');

const postCleaner = (postElem) => {
  // replace img emoji with unicode
  postElem.querySelectorAll('img.emoji').forEach(img => {
    const name = img.getAttribute('alt').replace(/:/g, '');
    const unicode = localStorage.getItem(name);
    if (unicode) {
      const textNode = document.createTextNode(unicode);
      img.parentNode.replaceChild(textNode, img);
    }
  });
  // remove avatar images
  postElem.querySelectorAll('img.avatar').forEach(img => img.remove());
  // replace mentions with text
  postElem.querySelectorAll('a.mention').forEach(a => {
    const textNode = document.createTextNode(a.textContent);
    a.parentNode.replaceChild(textNode, a);
  });
  // rewrite /t/ links to archive
  postElem.querySelectorAll('a[href*="/t/"]').forEach(a => {
    const match = a.href.match(/\/t\/([^\/]+)\/(\d+)/);
    if (match) {
      const slug = match[1];
      const id = match[2];
      a.href = `/t/${slug}/${id}`;
      a.className = 'internal';
      a.addEventListener('click', async e => {
        e.preventDefault();
        loadTopic(slug, id);
      });
    }
  });
  // replace onebox with link
  postElem.querySelectorAll('aside.onebox').forEach(aside => {
    const src = aside.getAttribute('data-onebox-src');
    const link = externalLink.cloneNode();
    link.href = src;
    link.textContent = `[ External Onebox ]`;
    aside.parentNode.replaceChild(link, aside);
  });
  // replace images with links
  postElem.querySelectorAll('img').forEach(img => {
    const link = externalLink.cloneNode();
    link.href = img.src;
    link.textContent = `[ External Image ]`;
    img.parentNode.replaceChild(link, img);
  });
}

// show topic
async function showTopic({ slug, url }) {
  mainEl.innerHTML = `<h2>Loading: ${slug}</h2><p>Fetching archive...</p>`;

  try {
    const topicData = await fetchJSON(url);
    const postsHTML = topicData.post_stream.posts.map(post => `<div class="post">
      <strong>${post.username}</strong> 
      <em>${new Date(post.created_at).toLocaleString()}</em>
      <div>${post.cooked}</div>
    </div>`).join('');
    // clean virtual DOM before inserting into real DOM
    // not really security risk since we're injecting anyways and already sanitized by discourse
    const domParser = new DOMParser();
    const virtualDom = domParser.parseFromString(postsHTML, 'text/html');
    // do all replacements
    postCleaner(virtualDom.body);
    // insert posts
    mainEl.innerHTML = `<h2>${topicData.title}</h2>${virtualDom.body.innerHTML}`;
  } catch(err) {
    mainEl.innerHTML = `<p style="color:red;">Failed to load topic: ${err}</p>`;
    console.error(err);
  }
}

// load topic from URL
async function loadInitialTopic() {
  const path = window.location.pathname;
  const parts = path.split('/').filter(Boolean);
  const [, slug, id] = parts;
  if (!slug || !id) return;
  if (id) await showTopic({ slug: slug, url: `/data/topics/${id}.json` });
  else mainEl.innerHTML = `<p style="color:red;">Topic not found: ${slug}</p>`;
}