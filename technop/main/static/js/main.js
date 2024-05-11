const items = document.getElementsByClassName('like-section');
const answer_like_section = document.getElementsByClassName('like-container');
const right_answer = document.getElementsByClassName('more-info');

function getCSRFToken() {
    // Extract the CSRF token from the cookie
    const cookieValue = document.cookie
        .split('; ')
        .find(row => row.startsWith('csrftoken='))
        .split('=')[1];

    return cookieValue;
}

const question_like_url = "/question_like";
const answer_like_url = "/answer_like";
const right_answer_url = "/right_answer";

const csrfToken = getCSRFToken();











// question_like
for (let it of items) {
    const [buttonLike, buttonDislike, text, counter] = it.children;
    buttonLike.addEventListener('click', () => {
        const headers = new Headers({
            'X-CSRFToken': csrfToken,
        });

        const formData = new FormData();
        formData.append('question_id', buttonLike.dataset.id);
        formData.append('value', buttonLike.dataset.value);

        const request = new Request(question_like_url, {
            method: 'POST',
            headers: headers,
            body: formData,
        });

        fetch(request)
            .then((response) => response.json())
            .then((data) => {
                console.log("Question Like Count:", data.count); // Логирование значения счетчика
                counter.innerHTML = data.count;
            });
    });

    buttonDislike.addEventListener('click', () => {
        const headers = new Headers({
            'X-CSRFToken': csrfToken,
        });

        const formData = new FormData();
        formData.append('question_id', buttonLike.dataset.id);

        const request = new Request(question_like_url, {
            method: 'POST',
            headers: headers,
            body: formData,
        });

        fetch(request)
            .then((response) => response.json())
            .then((data) => {
                console.log("Question Dislike Count:", data.count); // Логирование значения счетчика
                counter.innerHTML = data.count;
            });
    });
}






// answer_like
for (let it of answer_like_section) {
    const [buttonLike, buttonDislike, text, counter] = it.children;
    buttonLike.addEventListener('click', () => {
        const headers = new Headers({
            'X-CSRFToken': csrfToken,
        });

        const formData = new FormData();
        formData.append('answer_id', buttonLike.dataset.id);
        formData.append('value', buttonLike.dataset.value);

        const request = new Request(answer_like_url, {
            method: 'POST',
            headers: headers,
            body: formData,
        });

        fetch(request)
            .then((response) => response.json())
            .then((data) => {
                console.log("Answer Like Count:", data.count); // Логирование значения счетчика
                counter.innerHTML = data.count;
            });
    });

    buttonDislike.addEventListener('click', () => {
        const headers = new Headers({
            'X-CSRFToken': csrfToken,
        });

        const formData = new FormData();
        formData.append('answer_id', buttonLike.dataset.id);

        const request = new Request(answer_like_url, {
            method: 'POST',
            headers: headers,
            body: formData,
        });

        fetch(request)
            .then((response) => response.json())
            .then((data) => {
                console.log("Answer Dislike Count:", data.count); // Логирование значения счетчика
                counter.innerHTML = data.count;
            });
    });
}



// right_answer
for (let item of right_answer) {
    const [right_answer_change] = item.children;
    right_answer_change.checked = (right_answer_change.dataset.value === 'True');

    right_answer_change.addEventListener('click', () => {
        const headers = new Headers({
            'X-CSRFToken': csrfToken,
        });

        const formData = new FormData();
        formData.append('question_id', right_answer_change.dataset.question_id);
        formData.append('answer_id', right_answer_change.dataset.answer_id);
        formData.append('value', right_answer_change.dataset.value);

        const request = new Request('/right_answer', {
            method: 'POST',
            headers: headers,
            body: formData,
        });

        fetch(request)
            .then((response) => response.json())
            .then((data) => {
                console.log("Right Answer Count:", data.count); // Логирование значения счетчика
                right_answer_change.value = right_answer_change.dataset.value;
            })
            .catch((error) => {
                console.error('Error:', error);
            });
    });
}
