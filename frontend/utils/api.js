export const getToken = async () => {
    return String((await useFetch('/api/token/')).data.value)
}

export const postMeal = async (meal) => {
    let token = getToken()
    let form = new FormData()
    for (let id of meal.pets) form.append('pets', id)
    form.append('quantity', meal.quantity)
    form.append('food', meal.food)
    form.append('fed_at', meal.fed_at.toISOString())
    form.append('csrfmiddlewaretoken', await token)
    if (meal.id) 
        await useFetch(`/api/meal/${meal.id}/`, {
            method: 'PUT',
            body: form,
            headers: {'X-CSRFToken': useCookie('csrftoken')},
        })
    else
        await useFetch(`/api/meal/`, {
            method: 'POST',
            body: form,
        })
}

export const postPet = async (pet) => {
    let token = getToken()
    let form = new FormData()
    form.append('id', pet.id)
    form.append('name', pet.name)
    form.append('race', pet.race)
    form.append('description', pet.description)
    form.append('csrfmiddlewaretoken', await token)
    if (pet.id) 
        await useFetch(`/api/pet/${pet.id}/`, {
            method: 'PUT',
            body: form,
            headers: {'X-CSRFToken': useCookie('csrftoken')},
        })
    else
        await useFetch(`/api/pet/`, {
            method: 'POST',
            body: form,
        })
}

export const postFood = async (food) => {
    let token = getToken()
    let form = new FormData()
    let fields = ['id', 'name', 'brand', 'amount', 'num_packets', 'packet_size', 'category', 'price', 'unit']
    for (let field of fields) 
        form.append(field, food[field])
    form.append('csrfmiddlewaretoken', await token)
    if (food.id) 
        await useFetch(`/api/food/${food.id}/`, {
            method: 'PUT',
            body: form,
            headers: {'X-CSRFToken': useCookie('csrftoken')},
        })
    else
        await useFetch(`/api/food/`, {
            method: 'POST',
            body: form,
        })
}

export const postSchedule = async (schedule) => {
    let token = getToken()
    let form = new FormData()
    form.append('id', schedule.id)
    form.append('amount', schedule.amount)
    form.append('hour', schedule.hour)
    form.append('minute', schedule.minute)
    form.append('active', schedule.active)
    form.append('csrfmiddlewaretoken', await token)
    if (schedule.id) 
        await useFetch(`/api/schedules/${schedule.id}/`, {
            method: 'PUT',
            body: form,
            headers: {'X-CSRFToken': useCookie('csrftoken')},
        })
    else
        await useFetch(`/api/schedules/`, {
            method: 'POST',
            body: form,
        })
}

export const deleteFood = async (id) => {
    await useFetch(`/api/meal/${id}/`, {
        method: 'DELETE',
        headers: {'X-CSRFToken': useCookie('csrftoken')},
    })
}

export const deleteMeal = async (id) => {
    await useFetch(`/api/meal/${id}/`, {
        method: 'DELETE',
        headers: {'X-CSRFToken': useCookie('csrftoken')},
    })
}

export const deleteSchedule = async (id) => {
    await useFetch(`/api/schedules/${id}/`, {
        method: 'DELETE',
        headers: {'X-CSRFToken': useCookie('csrftoken')},
    })
}

export const deletePet = async (id) => {
    await useFetch(`/api/pet/${id}/`, {
        method: 'DELETE',
        headers: {'X-CSRFToken': useCookie('csrftoken')},
    })
}

export const getHelper = async () => {
    const result = useLazyFetch('/api/helper/', {
        // redirect to /login if status is 403
        onResponse({ response }) {
            if (response.status == 403) {
                navigateTo('/login')
            }
        }
    })
    return result
}

export const getMeals = async (date) => {
    const result = useLazyFetch('/api/meal/', {
        query: { date: date },
        // redirect to /login if status is 403
        onResponse({ response }) {
            if (response.status == 403) {
                navigateTo('/login')
            }
        }
    })
    return result
}

export const getPets = async () => {
    return useLazyFetch('/api/pet/',{
        onResponse({ response }) {
            if (response.status == 403) {
                navigateTo('/login')
            }
        }
    })
}

export const getFoods = async () => {
    return  useLazyFetch('/api/food/map/', {
        onResponse({ response }) {
            if (response.status == 403) {
                navigateTo('/login')
            }
        }
    })
}

export const getSchedules = async () => {
    return  useLazyFetch('/api/schedules/', {
        onResponse({ response }) {
            if (response.status == 403) {
                navigateTo('/login')
            }
        }
    })
}

export const getFoodOptions = async () => {
    return await useLazyFetch('/api/food/get_options', {
        onResponse({ response }) {
            if (response.status == 403) {
                navigateTo('/login')
            }
        }
    })
}

export const getDate = async (date) => {
    return new Date().toISOString().slice(0, 10)
}

export const logout = async () => {
    await useFetch('/api/auth/logout', {
    onResponse({ response }) {
        if (response.status == 200) navigateTo('/login')
    },
    })
}

export const postLogin = async (username, password) => {
    let form = new URLSearchParams()
    // get token
    let token = getToken()
    form.append('username', username)
    form.append('password', password)
    form.append('submit', 'Log in')
    form.append('next', '')
    form.append('csrfmiddlewaretoken', await token)
    return await useFetch('/api/login/', {
        method: 'POST',
        body: form,
        onResponse({ response }) {
            if (response.status == 200) navigateTo('/')
        }
    })
}
export const checkIfLoggedIn = async () => {
    await useFetch('/api/login', {
        onResponse({ response }) {
            if (response.status == 200) 
                navigateTo('/')
        }
    })
}

// function that turns timestamp into a date string HH:MM
export const toTimeString = (timestamp) => {
    return new Date(timestamp * 1000).toLocaleTimeString('de-DE', {
        hour: '2-digit',
        minute: '2-digit',
    }) + ' Uhr'
}

export const getScheduleTimeString = (hour, minute) => {
    let date = new Date()
    date.setHours(hour)
    date.setMinutes(minute)
    return date.toLocaleTimeString('de-DE', {
        hour: '2-digit',
        minute: '2-digit',
    }) + ' Uhr'
}

// function that turns date obj into YYYY-MM-DD with leading zeros
export const toDateString = (date) => {
    return `${date.getFullYear()}-${(date.getMonth()+1).toString().padStart(2,'0')}-${date.getDate().toString().padStart(2,'0')}`

}

export const connectToWebsocket = async (updateFunc, isConnected, isLoading) => {
    let protocol = window.location.protocol == 'https:' ? 'wss' : 'ws'
    var ws = new WebSocket(`${protocol}://${window.location.host}/ws/notify/`)
    var shouldReconnect = true
    ws.onopen = function() {
        if (!isConnected.value) updateFunc() 
        isLoading.value = false
        isConnected.value = 100
        console.log('WebSocket Client Connected')
    }
  
    ws.onmessage = function(e) { 
        updateFunc(e.data)
    }
  
    ws.onclose = function(e) {
        isConnected.value = 0
        if(shouldReconnect){
            console.log('Socket is closed. Reconnect will be attempted in 1 second.');
            setTimeout(function() { connectToWebsocket(updateFunc, isConnected, isLoading) }, 1000)
        }
    }
  
    ws.onerror = function(err) {
      console.error('Socket encountered error: Closing socket')
      ws.close()
    }
    ws.customClose = function() {
        shouldReconnect = false
        ws.close()
    }
    return ws
}