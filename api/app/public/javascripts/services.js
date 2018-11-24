// Show an object on the screen.
function showObject(obj) {
  const pre = document.getElementById('response');
  const preParent = pre.parentElement;
  pre.innerText = JSON.stringify(obj, null, 4);
  preParent.classList.add('flashing');
  setTimeout(() => preParent.classList.remove('flashing'), 300);
}

// Axios responses have a lot of data. This shows only the most relevant data.
function showResponse(axiosResponse) {
  const fullResponse = axiosResponse.response === undefined
    ? axiosResponse
    : axiosResponse.response;
  const abridgedResponse = {
    data: fullResponse.data,
    status: fullResponse.status,
    statusText: fullResponse.statusText,
  };
  showObject(abridgedResponse);
}

function handleSubmit(fields) {
  const body = JSON.parse(fields.body || '{}');
  axios[fields.method.toLowerCase()](fields.route, body)
    .then(showResponse)
    .catch(showResponse);
}

// attach handlers to forms
function init() {
  const form = document.getElementById('request-form');
  form.onsubmit = (e) => {
    e.preventDefault();
    const data = {};
    (new FormData(form)).forEach((value, key) => {
      data[key] = value;
    });
    handleSubmit(data);
    return false; // don't reload page
  };
}

window.onload = init; // attach handlers once DOM is ready
