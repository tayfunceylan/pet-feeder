export const getToken = async () => {
    return String((await useFetch('/api/token/')).data.value)
}

export const postMeal = async (food, quantity, pets, id) => {
    let token = getToken()
    let form = new FormData()
    for (let id of pets) form.append('pets', id)
    form.append('quantity', quantity)
    form.append('food', food)
    form.append('csrfmiddlewaretoken', await token)
    if (id) 
        await useFetch(`/api/meal/${id}/`, {
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

export const deleteMeal = async (id) => {
    await useFetch(`/api/meal/${id}/`, {
        method: 'DELETE',
        headers: {'X-CSRFToken': useCookie('csrftoken')},
    })
}

export const getMealsDate = async (date) => {
    if (!date) date = getDate()
    const result = await useFetch('/api/meal/sort_category/', {
        query: { date: await date },
        // redirect to /api/auth/login if status is 403
        onResponse({ response }) {
            if (response.status == 403) {
                window.location.href = '/api/auth/login'
            }
        }
    })
    return result
}

export const getPets = async () => {
    return (await useFetch('/api/pet/'))
}

export const getFoods = async () => {
    return (await useFetch('/api/food/'))
}

export const getDate = async (date) => {
    return new Date().toISOString().slice(0, 10)
}

export const logout = async () => {
    await useFetch('/api/auth/logout', {
    onResponse({ response }) {
        if (response.status == 200) window.location.href = '/api/auth/login'
    },
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
