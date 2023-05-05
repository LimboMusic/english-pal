let isHighlight = true;

function cancelBtnHandler() {
    cancelHighlighting();
    document.getElementById("text-content").removeEventListener("click", fillInWord, false);
    document.getElementById("text-content").removeEventListener("touchstart", fillInWord, false);
    document.getElementById("text-content").addEventListener("click", fillInWord2, false);
    document.getElementById("text-content").addEventListener("touchstart", fillInWord2, false);
}

function showBtnHandler() {
    document.getElementById("text-content").removeEventListener("click", fillInWord2, false);
    document.getElementById("text-content").removeEventListener("touchstart", fillInWord2, false);
    document.getElementById("text-content").addEventListener("click", fillInWord, false);
    document.getElementById("text-content").addEventListener("touchstart", fillInWord, false);
    highLight();
}

function getWord() {
    return window.getSelection ? window.getSelection() : document.selection.createRange().text;
}

function highLight() {
    if (!isHighlight) return;
    let articleContent = document.getElementById("article").innerText;
    let pickedWords = document.getElementById("selected-words");  // words picked to the text area
    let dictionaryWords = document.getElementById("selected-words2"); // words appearing in the user's new words list
    let allWords = pickedWords.value + " " + dictionaryWords.value;
    const list = allWords.split(" ");
    for (let i = 0; i < list.length; ++i) {
        list[i] = list[i].replace(/(^\s*)|(\s*$)/g, ""); //消除单词两边的空字符
        if (list[i] !== "" && "<mark>".indexOf(list[i]) === -1 && "</mark>".indexOf(list[i]) === -1) {
           //将文章中所有出现该单词word的地方改为："<mark>" + word + "<mark>"。 正则表达式RegExp()中，"\\b"代表单词边界匹配。

            //修改代码
            let articleContent_fb = articleContent;  //文章副本
            while(articleContent_fb.toLowerCase().indexOf(list[i].toLowerCase()) !== -1 && list[i]!=""){
                //找到副本中和list[i]匹配的第一个单词(第一种匹配情况),并赋值给list[i]。
                const index = articleContent_fb.toLowerCase().indexOf(list[i].toLowerCase());
                list[i] = articleContent_fb.substring(index, index + list[i].length);

                articleContent_fb = articleContent_fb.substring(index + list[i].length);    // 使用副本中list[i]之后的子串替换掉副本
                articleContent = articleContent.replace(new RegExp("\\b"+list[i]+"\\b","g"),"<mark>" + list[i] + "</mark>");
            }
        }
    }
    document.getElementById("article").innerHTML = articleContent;
}

function cancelHighlighting() {
    let articleContent = document.getElementById("article").innerText;
    let pickedWords = document.getElementById("selected-words");
    const dictionaryWords = document.getElementById("selected-words2");    
    const list = pickedWords.value.split(" ");    
    if (pickedWords != null) {
        for (let i = 0; i < list.length; ++i) {
            list[i] = list[i].replace(/(^\s*)|(\s*$)/g, "");
            if (list[i] !== "") {
                articleContent = articleContent.replace("<mark>" + list[i] + "</mark>", "list[i]");
            }
        }
    }
    if (dictionaryWords != null) {
        let list2 = pickedWords.value.split(" ");
        for (let i = 0; i < list2.length; ++i) {
            list2 = dictionaryWords.value.split(" ");
            list2[i] = list2[i].replace(/(^\s*)|(\s*$)/g, "");
            if (list2[i] !== "") {
                articleContent = articleContent.replace("<mark>" + list[i] + "</mark>", "list[i]");
            }
        }
    }
    document.getElementById("article").innerHTML = articleContent;
}

function fillInWord() {
    highLight();
}

function fillInWord2() {
    cancelHighlighting();
}

function toggleHighlighting() {
    if (isHighlight) {
        isHighlight = false;
        cancelHighlighting();
    } else {
        isHighlight = true;
        highLight();
    }
}

showBtnHandler();
