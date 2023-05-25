let isRead = true;
let isChoose = true;

function getWord() {
    return window.getSelection ? window.getSelection() : document.selection.createRange().text;
}

function fillInWord() {
    let word = getWord();
    if (isRead) Reader.read(word, inputSlider.value);
    if (!isChoose) return;
    const element = document.getElementById("selected-words");
    element.value = element.value + " " + word;
}

document.getElementById("text-content").addEventListener("click", fillInWord, false);

const sliderValue = document.getElementById("rangeValue");
const inputSlider = document.getElementById("rangeComponent");
inputSlider.oninput = () => {
    let value = inputSlider.value;
    sliderValue.textContent = value + '×';
};

function onReadClick() {
    isRead = !isRead;
}

function onChooseClick() {
    isChoose = !isChoose;
}
