var testApp = testApp || {};

testApp.init = function (postUrl, csrftoken, pubPrefix, host, port, useSSL) {
    this.postUrl = postUrl;
    this.csrftoken = csrftoken;
    this.pubPrefix = pubPrefix;

    if (host === null)
        host = window.location.hostname;

    if (port === null || port === '')
        port = window.location.port;

    if (useSSL === null) {
        useSSL = false;

        if (window.location.protocol === 'https:')
            useSSL = true;
    }

    this.pushstream = new PushStream({
        host: host,
        port: port,
        modes: "websocket",
        useSSL: useSSL
    });

    this.pushstream.onmessage = this.onMessage.bind(this);

};

testApp.sendMessage = function (message) {
    /* This sends a message to the web server (*not* to the pubsub queue),
    to a web page handled by Django (test_app.views.message_received)
    so the server can do parsing, checking, etc... or, in this case,
    send it back to the pubsub queue
     */

    var xhr = new XMLHttpRequest();

    xhr.open('POST', this.postUrl);
    xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
    xhr.setRequestHeader('X-CSRFToken', this.csrftoken);
    xhr.onload = function () {
        if (xhr.status !== 200) {
            alert('Request failed.  Returned status of ' + xhr.status);
        } else {
            testApp.setStatus("Server in response to published message said: " + xhr.responseText);
        }
    };
    xhr.send(encodeURI('message=' + message));
};

testApp.subscribe = function (channel) {
    this.pushstream.addChannel(this.pubPrefix + channel);
};

testApp.connect = function () {
    this.pushstream.connect();
};

testApp.clearOutput = function () {
    var output = document.getElementById("output");
    output.value = '';
}

testApp.writeLine = function (message) {
    var output = document.getElementById("output");
    output.value += message;
    output.value += '\r';
    output.scrollTop = output.scrollHeight; // output.scroll
};

testApp.onMessage = function (message) {
    this.writeLine("Incoming: " + message.message[0]);
};

testApp.setStatus = function (status) {
    document.getElementById('status').value = status;
}
