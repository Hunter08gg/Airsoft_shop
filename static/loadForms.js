async function loadCreaters() {
    const res = await fetch("/all-creaters/")
    const data = await res.json()
    data.forEach(creater => {
        const option = document.createElement("option")
        option.textContent = creater.name
        option.setAttribute("value", creater.id)
        const selectEl = document.querySelector("#creater")
        selectEl.appendChild(option)
    })
}

loadCreaters()
