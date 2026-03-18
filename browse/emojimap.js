// craft emoji map
const versionExpected = "2";

// validate version
if (localStorage.getItem("emojiMapVersion") != versionExpected) {
  // populate
  localStorage.clear()
  localStorage.setItem("emojiMapVersion", versionExpected);
  // fetch and set
  populateEmojiMap();
}

async function populateEmojiMap() {
  const emojiBase = "https://raw.githubusercontent.com/discourse/discourse-emojis/refs/heads/main/dist/"
  const emojis = await fetchJSON(emojiBase+"emojis.json")
  const aliases = await fetchJSON(emojiBase+"aliases.json")
  for (const emoji of emojis) {
    const unicode = emoji.code.split('-').map(cp => String.fromCodePoint(parseInt(cp, 16))).join('');
    localStorage.setItem(emoji.name, unicode);
    // set aliases
    const aliasMatch = aliases?.[emoji.name]
    if (!aliasMatch) continue;
    for (const alias of aliasMatch) {
      localStorage.setItem(alias, unicode);
    }
  }
}