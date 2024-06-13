function vigenereEncrypt(message, key) {
    let encrypted = "";
    let keyIndex = 0;
    for (let char of message) {
        if (!char.match(/[a-zA-Z]/)) {
            encrypted += char;
        } else {
            let shift = key[keyIndex % key.length].toUpperCase().charCodeAt(0) - 65;
            let shiftedChar = String.fromCharCode((char.toUpperCase().charCodeAt(0) - 65 + shift) % 26 + 65);
            encrypted += shiftedChar;
            keyIndex++;
        }
    }
    return encrypted;
}

function vigenereDecrypt(encrypted, key) {
    let decrypted = "";
    let keyIndex = 0;
    for (let char of encrypted) {
        if (!char.match(/[a-zA-Z]/)) {
            decrypted += char;
        } else {
            let shift = key[keyIndex % key.length].toUpperCase().charCodeAt(0) - 65;
            let shiftedChar = String.fromCharCode((char.toUpperCase().charCodeAt(0) - 65 - shift + 26) % 26 + 65);
            decrypted += shiftedChar;
            keyIndex++;
        }
    }
    return decrypted.toLowerCase();
}

async function getPasswordHash(password) {
    const encoder = new TextEncoder();
    const data = encoder.encode(password);

    const hashBuffer = await crypto.subtle.digest('SHA-256', data);

    const hashArray = Array.from(new Uint8Array(hashBuffer));
    const hashHex = hashArray.map(b => b.toString(16).padStart(2, '0')).join('');
    
    return hashHex;
}

function setCookie(name, value, options = {}) {
    // По умолчанию кука будет действовать до закрытия браузера
    let expires = options.expires;

    if (typeof expires == "number" && expires) {
        let d = new Date();
        d.setTime(d.getTime() + expires * 1000);
        expires = options.expires = d;
    }
    if (expires && expires.toUTCString) {
        options.expires = expires.toUTCString();
    }

    value = encodeURIComponent(value);

    let updatedCookie = name + "=" + value;

    for (let optionKey in options) {
        updatedCookie += "; " + optionKey;
        let optionValue = options[optionKey];
        if (optionValue !== true) {
            updatedCookie += "=" + optionValue;
        }
    }

    document.cookie = updatedCookie;
}

function getCookie(name) {
    let matches = document.cookie.match(new RegExp(
        "(?:^|; )" + name.replace(/([\.$?*|{}\(\)\[\]\\\/\+^])/g, '\\$1') + "=([^;]*)"
    ));
    return matches ? decodeURIComponent(matches[1]) : 'not-found';
}

function deleteCookie(name) {
    document.cookie = name + "=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;";
}