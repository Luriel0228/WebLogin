const loginForm = document.getElementById('login-form');
const signupForm = document.getElementById('signup-form');

loginForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const username = document.getElementById('login-username').value;
    const password = document.getElementById('login-password').value;

    // 로그인 처리 로직 (서버와 통신)
    try {
        const response = await fetch('/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ username, password }),
        });
        const data = await response.json();

        if (response.ok) {
            // 로그인 성공 처리
            console.log('로그인 성공');
        } else {
            console.error('로그인 실패:', data.error);
        }
    } catch (error) {
        console.error('오류:', error);
    }
});

signupForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const username = document.getElementById('signup-username').value;
    const password = document.getElementById('signup-password').value;

    // 회원가입 처리 로직 (서버와 통신)
    try {
        const response = await fetch('/signup', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ username, password }),
        });
        const data = await response.json();

        if (response.ok) {
            // 회원가입 성공 처리
            console.log('회원가입 성공');
        } else {
            console.error('회원가입 실패:', data.error);
        }
    } catch (error) {
        console.error('오류:', error);
    }
});
