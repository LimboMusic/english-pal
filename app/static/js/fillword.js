let isRead = true;
let isChoose = true;
let reader = window.speechSynthesis; // 全局定义朗读者，以便朗读和暂停
let current_position = 0; // 朗读文本的当前位置
let original_position = 0; // 朗读文本的初始位置
let to_speak = ""; // 朗读的初始内容

function getWord() {
    return window.getSelection ? window.getSelection() : document.selection.createRange().text;
}

function fillInWord() {
    let word = getWord();
    if (isRead) read(word);
    if (!isChoose) return;
    const element = document.getElementById("selected-words");
    element.value = element.value + " " + word;
}

document.getElementById("text-content").addEventListener("click", fillInWord, false);

function makeUtterance(str, rate) {
    let msg = new SpeechSynthesisUtterance(str);
    msg.rate = rate;
    msg.lang = "en-US"; // TODO: add language options menu
    msg.onboundary = ev => {
        if (ev.name == "word") {
            current_position = ev.charIndex;
        }
    }
    return msg;
}

const sliderValue = document.getElementById("rangeValue"); // 显示值
const inputSlider = document.getElementById("rangeComponent"); // 滑块元素
inputSlider.oninput = () => {
    let value = inputSlider.value; // 获取滑块的值
    sliderValue.textContent = value + '×';
    if (!reader.speaking) return;
    reader.cancel();
    let msg = makeUtterance(to_speak.substring(original_position + current_position), value);
    original_position = original_position + current_position;
    current_position = 0;
    reader.speak(msg);
};

function read(s) {
    to_speak = s.toString();
    original_position = 0;
    current_position = 0;
    let msg = makeUtterance(to_speak, inputSlider.value);
    reader.speak(msg);
}

function onReadClick() {
    isRead = !isRead;
    if (!isRead) {
        reader.cancel();
    }
}

function onChooseClick() {
    isChoose = !isChoose;
}

function stopRead() {
    reader.cancel();
}