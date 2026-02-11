// craft emoji map
const emojiMap = new Map();
const emojis = fetchJSON("https://raw.githubusercontent.com/discourse/discourse-emojis/refs/heads/main/dist/emojis.json")
  .then(data => {
    for (const emoji of data) {
      emojiMap.set(emoji.name, emoji.code.split('-').map(cp => String.fromCodePoint(parseInt(cp, 16))).join(''));
    }
  })
// map aliases
const aliases = fetchJSON("https://raw.githubusercontent.com/discourse/discourse-emojis/refs/heads/main/dist/aliases.json")
  .then(data => {
    for (const [name, aliases] of Object.entries(data)) {
      const unicode = emojiMap.get(name);
      for (const alias of aliases) {
        emojiMap.set(alias, unicode);
      }
    }
  })