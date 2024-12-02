document.addEventListener("DOMContentLoaded", function() {
  const containerDate = document.getElementById("container-date");

  const dates = getDate();

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
    divMorning.setAttribute('data-date', date);
    divDay.className = "btn btn-primary";
    divDay.setAttribute('data-date', date);
    divEvening.className = "btn btn-primary";
    divEvening.setAttribute('data-date', date);

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

  containerDate.appendChild(divBack)
  containerDate.appendChild(divNext)
});

function getDate() {
  let today = new Date(page = 0);

  today.setDate(today.getDate() + (page * 10));

  let dates = [];

  for (let i = 0; i < 10; i++) {
      let date = new Date(today);
      date.setDate(today.getDate() + i);
      dates.push(date.toISOString().split('T')[0]);
  }

  console.log(dates);

  return dates
}

function setDate(event) {
  if(event.target.dataset.isSelected) {
    event.target.dataset.isSelected = ""
    event.target.innerHTML = ""
  } else {
    event.target.dataset.isSelected = "active"
    event.target.innerHTML = "✅"
  }
  console.log("event: ", event)
}