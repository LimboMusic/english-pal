function familiar(theWord) {
    let username = $("#username").text();
    let word = $("#word_" + theWord).text();
    let freq = $("#freq_" + theWord).text();
    $.ajax({
        type:"GET",
        url:"/" + username + "/" + word + "/familiar",
        success:function(response){
            let new_freq = freq - 1;
            const allow_move = document.getElementById("move_dynamiclly").checked;
            if (allow_move) {

                if (new_freq <= 0) {
                    removeWord(theWord);
                } else {
                    renderWord({ word: theWord, freq: new_freq });
                }
            } else {
                if(new_freq <1) {
                    $("#p_" + theWord).remove();
                } else {
                    $("#freq_" + theWord).text(new_freq);
                }
            }
        }
    });
}

function unfamiliar(theWord) {
    let username = $("#username").text();
    let word = $("#word_" + theWord).text();
    let freq = $("#freq_" + theWord).text();
    $.ajax({
        type:"GET",
        url:"/" + username + "/" + word + "/unfamiliar",
        success:function(response){
            let new_freq = parseInt(freq) + 1;
            const allow_move = document.getElementById("move_dynamiclly").checked;
            if (allow_move) {
                renderWord({ word: theWord, freq: new_freq });
            } else {
                $("#freq_" + theWord).text(new_freq);
            }
        }
    });
}

function delete_word(theWord) {
    let username = $("#username").text();
    let word = theWord.replace('&amp;', '&');
    $.ajax({
        type:"GET",
        url:"/" + username + "/" + word + "/del",
        success:function(response){
            const allow_move = document.getElementById("move_dynamiclly").checked;
            if (allow_move) {
                removeWord(theWord);
            } else {
                $("#p_" + theWord).remove();
            }    
        }
    });
}

/* 
 * interface Word {
 *   word: string,
 *   freq: number
 * }
* */

/**
 * 传入一个词频HTML元素，将其解析为Word类型的对象
 */
function parseWord(element) {
    const word = element
        .querySelector("a.btn.btn-light[role=button]")  // 获取当前词频元素的词汇元素
        .innerText  // 获取词汇值;
    const freq = Number.parseInt(element.querySelector(`#freq_${word}`).innerText);   // 获取词汇的数量
    return {
        word,
        freq
    };
}

/**
 * 使用模板将传入的单词转换为相应的HTML字符串
*/
function wordTemplate(word) {
    // 这个模板应当与 templates/userpage_get.html 中的 <p id='p_${word.word}' class="new-word" > ... </p> 保持一致
    return `<p id='p_${word.word}' class="new-word" >
        <a id="word_${word.word}"  class="btn btn-light" href='http://youdao.com/w/eng/${word.word}/#keyfrom=dict2.index'
           role="button">${word.word}</a>
        ( <a id="freq_${word.word}" title="${word.word}">${word.freq}</a> )
        <a class="btn btn-success" onclick="familiar('${word.word}')" role="button">熟悉</a>
        <a class="btn btn-warning" onclick="unfamiliar('${word.word}')" role="button">不熟悉</a>
        <a class="btn btn-danger" onclick="delete_word('${word.word}')" role="button">删除</a>
    </p>`;
}

/**
 * 删除某一词频元素
 * 此处word为词频元素对应的单词
 */
function removeWord(word) {
    // 根据词频信息删除元素
    word = word.replace('&amp;', '&');
    const element_to_remove = document.getElementById(`p_${word}`);
    if (element_to_remove != null) {
        element_to_remove.remove();
    }
}

function renderWord(word) {
    const container = document.querySelector(".word-container");
    // 删除原有元素
    removeWord(word.word);
    // 插入新元素
    let inserted = false;
    const new_element = elementFromString(wordTemplate(word));
    for (const current of container.children) {
        const cur_word = parseWord(current);
        // 找到第一个词频比它小的元素，插入到这个元素前面
        if (compareWord(cur_word, word) == -1) {
            container.insertBefore(new_element, current);
            inserted = true;
            break;
        }
    }
    // 当word就是词频最小的词时，把他补回去
    if (!inserted) {
        container.appendChild(new_element);
    }
    // 让发生变化的元素抖动
    new_element.classList.add("shaking");
    // 移动到该元素
    new_element.scrollIntoView({behavior: "smooth", block: "center", inline: "nearest"});
    // 抖动完毕后删除抖动类
    setTimeout(() => {
        new_element.classList.remove("shaking");
    }, 1600);
}

/**
 * 从string中创建一个HTML元素并返回
 */
function elementFromString(string) {
    const d = document.createElement('div');
    d.innerHTML = string;
    return d.children.item(0);
}

/**
 * 对比两个单词：
 *  当first小于second时返回-1
 *  当first等于second时返回0
 *  当first大于second时返回1
 */
function compareWord(first, second) {
    if (first.freq < second.freq) {
        return -1;
    }
    if (first.freq > second.freq) {
        return 1;
    }
    if (first.word < second.word) {
        return -1;
    }
    if (first.word > second.word) {
        return 1;
    }
    return 0;
}
