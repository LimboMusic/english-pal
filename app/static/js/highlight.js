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
    let articleContent = document.getElementById("article").innerText; //将原来的.innerText改为.innerHtml，使用innerText会把原文章中所包含的<br>标签去除，导致处理后的文章内容失去了原来的格式
    let pickedWords = document.getElementById("selected-words");  // words picked to the text area
    let dictionaryWords = document.getElementById("selected-words2"); // words appearing in the user's new words list
    let allWords = "";  //初始化allWords的值，避免进入判断后编译器认为allWords未初始化的问题
    if(dictionaryWords != null){//增加一个判断，检查生词本里面是否为空，如果为空，allWords只添加选中的单词
        allWords = pickedWords.value + " " + dictionaryWords.value;
    }
    else{
        allWords = pickedWords.value + " ";
    }
    const list = allWords.split(" ");//将所有的生词放入一个list中，用于后续处理
    for (let i = 0; i < list.length; ++i) {
        list[i] = list[i].replace(/(^\s*)|(\s*$)/g, ""); //消除单词两边的空字符
        list[i] = list[i].replace('|', "");
        list[i] = list[i].replace('?', "");
        if (list[i] !== "" && "<mark>".indexOf(list[i]) === -1 && "</mark>".indexOf(list[i]) === -1) {
           //将文章中所有出现该单词word的地方改为："<mark>" + word + "<mark>"。 正则表达式RegExp()中，"\\b"代表单词边界匹配。

            //修改代码
            let articleContent_fb = articleContent;  //文章副本
            let count = 1000;  //简单计数器，防止陷入死循环。
            while(articleContent_fb.toLowerCase().indexOf(list[i].toLowerCase()) !== -1 && list[i]!=""){
                //针对同一篇文章中可能存在相同单词的不同大小写问题，采用while循环判断副本中是否还存在匹配单词。

                count--;
                if(count <= 0)break;   //TimeOut!

                //找到副本中和list[i]匹配的第一个单词(第一种匹配情况),并赋值给list[i]。
                list[i] = articleContent_fb.substr(articleContent_fb.toLowerCase().indexOf(list[i].toLowerCase()),list[i].length);

                articleContent_fb = articleContent_fb.replace(list[i],""); //删除副本中和list[i]匹配的单词
                articleContent = articleContent.replace(new RegExp("\\b"+list[i]+"\\b","g"),"<mark>" + list[i] + "</mark>");
            }
        }
    }
    document.getElementById("article").innerHTML = articleContent;
}

function cancelHighlighting() {
    let articleContent = document.getElementById("article").innerText;//将原来的.innerText改为.innerHtml，原因同上
    let pickedWords = document.getElementById("selected-words");
    const dictionaryWords = document.getElementById("selected-words2");    
    const list = pickedWords.value.split(" ");    
    if (pickedWords != null) {
        for (let i = 0; i < list.length; ++i) {
            list[i] = list[i].replace(/(^\s*)|(\s*$)/g, "");
            if (list[i] !== "") { //原来判断的代码中，替换的内容为“list[i]”这个字符串，这明显是错误的，我们需要替换的是list[i]里的内容
                articleContent = articleContent.replace(new RegExp("<mark>"+list[i]+"</mark>", "g"), list[i]);
            }
        }
    }
    if (dictionaryWords != null) {
        let list2 = pickedWords.value.split(" ");
        for (let i = 0; i < list2.length; ++i) {
            list2 = dictionaryWords.value.split(" ");
            list2[i] = list2[i].replace(/(^\s*)|(\s*$)/g, "");
            if (list2[i] !== "") { //原来代码中，替换的内容为“list[i]”这个字符串，这明显是错误的，我们需要替换的是list[i]里的内容
                articleContent = articleContent.replace(new RegExp("<mark>"+list2[i]+"</mark>", "g"), list2[i]);
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
