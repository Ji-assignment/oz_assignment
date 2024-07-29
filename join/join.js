const form = document.getElementById("form");

form.addEventListener("submit", function(event) {
    event.preventDefault();

    let userId = event.target.id.value;
    let userPw1 = event.target.pw1.value;
    let userPw2 = event.target.pw2.value;

    if (userId.length < 6) {
        alert("아이디가 너무 짧습니다. 6자 이상 입력해주세요.");
        return;
    }

    if (userPw1 !== userPw2) {
        alert("비밀번호가 일치하지 않습니다.");
        return;
    }

    const message = document.createElement('p');
    message.textContent = `${userId}님 환영합니다.`;
    document.body.innerHTML = "";
    document.body.appendChild(message);

    console.log(userId, userPw1, userPw2);
});
