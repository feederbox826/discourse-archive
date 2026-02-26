const topicListEl = document.getElementById('topicList');

async function loadTopic(slug, id) {
  history.pushState({}, '', `/t/${slug}/${id}`);
  await showTopic({ title: slug, url: `/data/topics/${id}.json` });
}

let topicJSON = []
let currentData = []

async function loadIndex() {
  try {
    topicJSON = await fetchJSON("/data/topics/index.json");
    for (const topic of topicJSON) {
      const [ id, slug, title, , replies ] = topic;
      const a = document.createElement('a');
      a.textContent = title + (replies ? ` (${replies})` : '');
      a.href = `/t/${slug}/${id}`;
      a.className = 'topic-link';
      a.addEventListener('click', async e => {
        e.preventDefault();
        loadTopic(slug, id);
      });
      topicListEl.appendChild(a);
    };
    // Auto-load topic from path/query
    await loadInitialTopic();
  } catch(err) {
    alert('Failed to load index: ' + err);
    console.error(err);
  }
  renderTable(topicJSON);
  currentData = topicJSON;
};

// create table
const tableBody = document.querySelector('#topicTable tbody');
function renderTable(data) {
  tableBody.innerHTML = '';
  data.forEach(([id, slug, title, lastUpdated, replies]) => {
    const tr = document.createElement('tr');
    tr.innerHTML = `
      <td>
        <a class="topic-link" href="/t/${slug}/${id}">${title}</a>
      </td>
      <td>${new Date(lastUpdated).toLocaleDateString()}</td>
      <td>${replies}</td>
    `;
    // add click listener to load topic
    tr.querySelector('a').addEventListener('click', async e => {
      e.preventDefault();
      loadTopic(slug, id);
    });

    tableBody.appendChild(tr);
  });
}
// search
document.getElementById('topicSearch').addEventListener('input', (e) => {
  const q = e.target.value.toLowerCase();
  currentData = topicJSON.filter(([,,title]) => title.toLowerCase().includes(q));
  renderTable(currentData);
});
// sorting
document.querySelectorAll('#topicTable th').forEach(th => {
  th.addEventListener('click', () => {
    const key = th.dataset.sort

    currentData.sort((a, b) => {
      if (key === 'title') return a[2].localeCompare(b[2]);
      if (key === 'last_updated') return new Date(b[3]) - new Date(a[3]);
      if (key === 'reply_count') return b[4] - a[4];
    })
    renderTable(currentData)
  })
})
loadIndex();
window.addEventListener('popstate', async () => { await loadInitialTopic(); });
