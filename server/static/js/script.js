let datesSelect = []
let timesSelect = []
let inputDate

document.addEventListener("DOMContentLoaded", function() {
  inputDate = document.getElementById("input-date");
  getDate()
  getTime()
});

function getDate(page = 0) {
  const containerDate = document.getElementById("container-date");

  containerDate.innerHTML = "";

  let today = new Date();

  const dates = [];

  today.setDate(today.getDate() + (page * 10));

  for (let i = 0; i < 10; i++) {
      let date = new Date(today);
      date.setDate(today.getDate() + i);
      dates.push(date.toISOString().split('T')[0]);
  }

  const divDateTitle = document.createElement('div');
  const divMorningTitle = document.createElement('div');
  const divDayTitle = document.createElement('div');
  const divEveningTitle = document.createElement('div');

  divDateTitle.innerHTML = "Дата";
  divMorningTitle.innerHTML = "Утро";
  divDayTitle.innerHTML = "День";
  divEveningTitle.innerHTML = "Вечер";

  divDateTitle.className = "btn btn-primary";
  divMorningTitle.className = "btn btn-primary";
  divDayTitle.className = "btn btn-primary";
  divEveningTitle.className = "btn btn-primary";


  containerDate.appendChild(divDateTitle)
  containerDate.appendChild(divMorningTitle)
  containerDate.appendChild(divDayTitle)
  containerDate.appendChild(divEveningTitle)

  for(const date of dates) {
    const divDate = document.createElement('div');
    const divMorning = document.createElement('div');
    const divDay = document.createElement('div');
    const divEvening = document.createElement('div');

    divDate.className = "btn btn-primary";
    divDate.innerHTML = date;

    divMorning.className = "btn btn-primary";
    divMorning.setAttribute('data-date', `${date}/УТРО`);
    if(datesSelect.includes(`${date}/УТРО`)) {
      divMorning.setAttribute('data-is-selected', 'active');
      divMorning.innerHTML ="✅"
    }

    divDay.className = "btn btn-primary";
    divDay.setAttribute('data-date', `${date}/ДЕНЬ`);
    if(datesSelect.includes(`${date}/ДЕНЬ`)) {
      divDay.setAttribute('data-is-selected', 'active');
      divDay.innerHTML ="✅"
    }

    divEvening.className = "btn btn-primary";
    divEvening.setAttribute('data-date', `${date}/ВЕЧЕР`);
    if(datesSelect.includes(`${date}/ВЕЧЕР`)) {
      divEvening.setAttribute('data-is-selected', 'active');
      divEvening.innerHTML ="✅"
    }

    divMorning.addEventListener("click", setDate)
    divDay.addEventListener("click", setDate)
    divEvening.addEventListener("click", setDate)

    containerDate.appendChild(divDate)
    containerDate.appendChild(divMorning)
    containerDate.appendChild(divDay)
    containerDate.appendChild(divEvening)
  }

  const divBack = document.createElement('div');
  const divNext = document.createElement('div');

  divBack.innerHTML = "Назад";
  divNext.innerHTML = "Вперед";

  divBack.className = "last-row btn btn-primary";
  divNext.className = "last-row btn btn-primary";

  divBack.addEventListener("click", () => getDate(page - 1 <= 0? 0: page - 1))
  divNext.addEventListener("click", () => getDate(page + 1))

  containerDate.appendChild(divBack)
  containerDate.appendChild(divNext)
}

function setDate(event) {
  if(event.target.dataset.isSelected) {
    event.target.dataset.isSelected = ""
    event.target.innerHTML = ""
    const inputDateValueArray = inputDate.value.split(" ").filter(date => date !== event.target.dataset.date)
    inputDate.value = inputDateValueArray.join(" ")
  } else {
    event.target.dataset.isSelected = "active"
    event.target.innerHTML = "✅"
    inputDate.value = ((inputDate.value? inputDate.value: '') + ' ' + event.target.dataset.date).trim();
  }
  console.log("inputDate.value: ", inputDate.value)
}

function nextDate(event) {
  if(event.target.dataset.isSelected) {
    event.target.dataset.isSelected = ""
    event.target.innerHTML = ""
  } else {
    event.target.dataset.isSelected = "active"
    event.target.innerHTML = "✅"
  }
}

function getTime() {
  const containerTime = document.getElementById("container-time");

  containerTime.innerHTML = "";

  const times = ['8/10', '13/10', '18/10', '9/10', '14/10', '19/10', '10/10', '15/10', '20/10', '11/10', '16/10', '21/10', '12/10', '17/10', '22/10']

  const divMorningTitle = document.createElement('div');
  const divDayTitle = document.createElement('div');
  const divEveningTitle = document.createElement('div');

  divMorningTitle.innerHTML = "Утро";
  divDayTitle.innerHTML = "День";
  divEveningTitle.innerHTML = "Вечер";

  divMorningTitle.className = "btn btn-primary";
  divDayTitle.className = "btn btn-primary";
  divEveningTitle.className = "btn btn-primary";


  containerTime.appendChild(divMorningTitle)
  containerTime.appendChild(divDayTitle)
  containerTime.appendChild(divEveningTitle)

  for(const time of times) {
    const divTime = document.createElement('div');

    divTime.className = "btn btn-primary";
    divTime.innerHTML = time;

    divTime.addEventListener("click", setTime)

    containerTime.appendChild(divTime)
  }
}

function setTime(event) {
  if(event.target.dataset.isSelected) {
    event.target.dataset.isSelected = ""
    event.target.innerHTML = ""
    const inputDateValueArray = inputDate.value.split(" ").filter(date => date !== event.target.dataset.date)
    inputDate.value = inputDateValueArray.join(" ")
  } else {
    event.target.dataset.isSelected = "active"
    event.target.innerHTML = "✅"
    inputDate.value = ((inputDate.value? inputDate.value: '') + ' ' + event.target.dataset.date).trim();
  }
  console.log("inputDate.value: ", inputDate.value)
}
