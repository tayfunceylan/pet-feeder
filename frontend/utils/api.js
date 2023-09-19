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

export const deletePet = async (id) => {
    await useFetch(`/api/pet/${id}/`, {
        method: 'DELETE',
        headers: {'X-CSRFToken': useCookie('csrftoken')},
    })
}

export const getMealsDate = async (date) => {
    if (!date) date = getDate()
    const result = await useFetch('/api/meal/sort_category/', {
        query: { date: await date },
        // redirect to /login if status is 403
        onResponse({ response }) {
            if (response.status == 403) {
                window.location.href = '/login'
            }
        }
    })
    return result
}

export const getHelper = async () => {
    const result = await useFetch('/api/helper/', {
        // redirect to /login if status is 403
        onResponse({ response }) {
            if (response.status == 403) {
                window.location.href = '/login'
            }
        }
    })
    return result
}

export const getMeals = async (date) => {
    const result = await useFetch('/api/meal/get_day/', {
        query: { date: date },
        // redirect to /login if status is 403
        onResponse({ response }) {
            if (response.status == 403) {
                window.location.href = '/login'
            }
        }
    })
    return result
}

export const getPets = async () => {
    return await useFetch('/api/pet/',{
        onResponse({ response }) {
            if (response.status == 403) {
                window.location.href = '/login'
            }
        }
    })
}

export const getFoods = async () => {
    return (await useFetch('/api/food/', {
        onResponse({ response }) {
            if (response.status == 403) {
                window.location.href = '/login'
            }
        }
    }))
}

export const getFoodOptions = async () => {
    return (await useFetch('/api/food/get_options', {
        onResponse({ response }) {
            if (response.status == 403) {
                window.location.href = '/login'
            }
        }
    }))
}

export const getDate = async (date) => {
    return new Date().toISOString().slice(0, 10)
}

export const logout = async () => {
    await useFetch('/api/auth/logout', {
    onResponse({ response }) {
        if (response.status == 200) window.location.href = '/login'
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
            if (response.status == 200) window.location.href = '/'
        }
    })
}
export const checkIfLoggedIn = async () => {
    await useFetch('/api/login', {
        onResponse({ response }) {
            if (response.status == 200) 
                window.location.href = '/'
        }
    })
}

export const reduceList = (list) => {
    return list.reduce(
    (obj, item) => {
        obj[item.id] = item
        return obj
    }, {})
}

// function that turns timestamp into a date string HH:MM
export const toTimeString = (timestamp) => {
    return new Date(timestamp * 1000).toLocaleTimeString('de-DE', {
        hour: '2-digit',
        minute: '2-digit',
    }) + ' Uhr'
}

export const connectToWebsocket = async (updateFunc, isConnected) => {
    let protocol = window.location.protocol == 'https:' ? 'wss' : 'ws'
    var ws = new WebSocket(`${protocol}://${window.location.host}/ws/notify/`)
    var shouldReconnect = true
    ws.onopen = function() {
        if (!isConnected.value) updateFunc() 
        isConnected.value = 100
        console.log('WebSocket Client Connected')
    }
  
    ws.onmessage = updateFunc
  
    ws.onclose = function(e) {
        isConnected.value = 0
        if(shouldReconnect){
            console.log('Socket is closed. Reconnect will be attempted in 1 second.');
            setTimeout(function() { connectToWebsocket(updateFunc, isConnected) }, 1000)
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