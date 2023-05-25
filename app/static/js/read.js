// read.js
var Reader = (function() {
    let reader = window.speechSynthesis;
    let current_position = 0;
    let original_position = 0;
    let to_speak = "";

    function makeUtterance(str, rate) {
        let msg = new SpeechSynthesisUtterance(str);
        msg.rate = rate;
        msg.lang = "en-US";
        msg.onboundary = ev => {
            if (ev.name == "word") {
                current_position = ev.charIndex;
            }
        }
        return msg;
    }

    function read(s, rate) {
        to_speak = s.toString();
        original_position = 0;
        current_position = 0;
        let msg = makeUtterance(to_speak, rate);
        reader.speak(msg);
    }

    function stopRead() {
        reader.cancel();
    }

    return {
        read: read,
        stopRead: stopRead
    };
})();
