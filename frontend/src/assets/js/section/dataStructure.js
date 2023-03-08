export default class Trie {
  constructor(isOri) {
    this.isOri = isOri;
    this.tree = {};
  }
  insert(word) {
    let tree = this.tree;
    const wordArray = word.split('.');
    for (let i = 0; i < wordArray.length; i++) {
      if (tree[wordArray[i]] == undefined) {
        tree[wordArray[i]] = {};
      }
      tree = tree[wordArray[i]];
    }
  }
  DFS(array, str) {
    return array.map((e) => {
      let children = [];
      const qualifiedName = str === '' ? `${e[0]}` : `${str}.${e[0]}`;
      const temp = Object.entries(e[1]);
      if (temp.length) {
        children = this.DFS(temp, qualifiedName);
      }
      const item = {
        name: e[0],
        qualifiedName,
        id: `${qualifiedName}_${this.isOri ? 0 : 1}`,
        isOri: this.isOri,
      };
      if (children.length) {
        item.children = children;
      } else {
        item.value = 1;
      }
      return item;
    });
  }
  fileDFS(array, str) {
    return array.map((e) => {
      let name = '';
      let children = [];
      let qualifiedName = str === '' ? `${e[0]}` : `${str}.${e[0]}`;
      let temp = Object.entries(e[1]);
      if (temp.length) {
        if (temp.length === 1) {
          [temp, name, qualifiedName] = this.straight(temp, e[0], qualifiedName);
        }
        children = this.fileDFS(temp, qualifiedName);
      }
      const item = {
        name: name === '' ? e[0] : name,
        qualifiedName,
        id: `${qualifiedName}_${this.isOri ? 0 : 1}`,
        isOri: this.isOri,
      };
      if (children.length) {
        item.children = children;
      } else {
        item.value = 1;
      }
      return item;
    });
  }
  // 合并点
  straight(array, str, qName) {
    const name = `${str}.${array[0][0]}`;
    const qualifiedName = `${qName}.${array[0][0]}`;
    const temp = Object.entries(array[0][1]);
    let result = [temp, name, qualifiedName];
    if (temp.length === 1) {
      result = this.straight(temp, name, qualifiedName);
    }
    return result;
  }
  result() {
    return this.DFS(Object.entries(this.tree), '');
  }
  fileResult() {
    return this.fileDFS(Object.entries(this.tree), '');
  }
}
