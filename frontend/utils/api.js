// you need X-CSRFToken header for PUT and DELET Requests
// you dont need it for get and post requests

export const useLoading = () => useState("isLoading", () => true);
export const ownFetch = (url, options, cache) => {
  const ws = useWebsocketStore();
  const config = useRuntimeConfig();
  options = {
    ...options,
    credentials: "include",
    baseURL: config.public.baseURL,
    onRequest() {
      ws.isLoading = true;
    },
    onResponse({ response }) {
      ws.isLoading = false;
      if (response.status == 403) navigateTo("/login");
    },
  };
  if (cache) return useFetch(url, options);
  else return $fetch(url, options);
};

export const ownUseFetch = (url, options) => {
  return ownFetch(url, options, true);
};

export const ownUseFetchOnce = (url, options) => {
  return ownFetch(url, options, false);
};

export const ownUseLazyFetch = (url, options) => {
  options = options || {};
  options.lazy = true;
  return ownUseFetch(url, options);
};

export const getToken = async () => {
  return await ownUseFetchOnce("/api/token/");
};

export const postMeal = async (meal) => {
  let token = getToken();
  let form = new FormData();
  for (let id of meal.pets) form.append("pets", id);
  form.append("quantity", meal.quantity);
  form.append("food", meal.food);
  form.append("fed_at", meal.fed_at.toISOString());
  form.append("csrfmiddlewaretoken", await token);
  if (meal.id)
    await ownUseFetchOnce(`/api/meal/${meal.id}/`, {
      method: "PUT",
      body: form,
      headers: { "X-CSRFToken": await token },
    });
  else
    await ownUseFetchOnce(`/api/meal/`, {
      method: "POST",
      body: form,
    });
};

export const postPet = async (pet) => {
  let token = getToken();
  let form = new FormData();
  // pet.picture is a file object
  form.append("id", pet.id);
  form.append("name", pet.name);
  form.append("race", pet.race);
  form.append("birthday_on", pet.birthday_on);
  form.append("description", pet.description);
  if (pet.image) form.append("picture", pet.image[0]);
  form.append("csrfmiddlewaretoken", await token);
  if (pet.id)
    await ownUseFetchOnce(`/api/pet/${pet.id}/`, {
      method: "PUT",
      body: form,
      headers: { "X-CSRFToken": await getToken() },
    });
  else
    await ownUseFetchOnce(`/api/pet/`, {
      method: "POST",
      body: form,
    });
};

export const postFood = async (food) => {
  let token = getToken();
  let form = new FormData();
  let fields = [
    "id",
    "name",
    "brand",
    "amount",
    "num_packets",
    "packet_size",
    "category",
    "price",
    "unit",
    "active",
  ];
  for (let field of fields) form.append(field, food[field]);
  form.append("csrfmiddlewaretoken", await token);
  if (food.id)
    await ownUseFetchOnce(`/api/food/${food.id}/`, {
      method: "PUT",
      body: form,
      headers: { "X-CSRFToken": await getToken() },
    });
  else
    await ownUseFetchOnce(`/api/food/`, {
      method: "POST",
      body: form,
    });
};

export const postSchedule = async (schedule) => {
  let token = getToken();
  let form = new FormData();
  form.append("id", schedule.id);
  form.append("amount", schedule.amount);
  form.append("hour", schedule.hour);
  form.append("minute", schedule.minute);
  form.append("active", schedule.active);
  form.append("csrfmiddlewaretoken", await token);
  if (schedule.id)
    await ownUseFetchOnce(`/api/schedules/${schedule.id}/`, {
      method: "PUT",
      body: form,
      headers: { "X-CSRFToken": await getToken() },
    });
  else
    await ownUseFetchOnce(`/api/schedules/`, {
      method: "POST",
      body: form,
    });
};

export const deleteMeal = async (id) => {
  await ownUseFetchOnce(`/api/meal/${id}/`, {
    method: "DELETE",
    headers: { "X-CSRFToken": await getToken() },
  });
};

export const deleteSchedule = async (id) => {
  await ownUseFetchOnce(`/api/schedules/${id}/`, {
    method: "DELETE",
    headers: { "X-CSRFToken": await getToken() },
  });
};

export const deletePet = async (id) => {
  await ownUseFetchOnce(`/api/pet/${id}/`, {
    method: "DELETE",
    headers: { "X-CSRFToken": await getToken() },
  });
};

export const getFoodID = async (id) => {
  await ownUseFetch(`/api/meal/${id}/`, {
    method: "GET",
  });
};
export const getMealID = async (id) => {
  await ownUseFetch(`/api/meal/${id}/`, {
    method: "GET",
  });
};

export const getHelper = () => {
  return ownUseLazyFetch("/api/helper/");
};

export const getMeals = (date) => {
  return ownUseLazyFetch("/api/meal/", { query: { date: date } });
};

export const getPets = () => {
  return ownUseLazyFetch("/api/pet/");
};

export const getFoods = () => {
  return ownUseLazyFetch("/api/food/");
};

export const getSchedules = () => {
  return ownUseLazyFetch("/api/schedules/");
};

export const getFoodOptions = () => {
  return ownUseLazyFetch("/api/food/get_options");
};

export const getDate = async (date) => {
  return new Date().toISOString().slice(0, 10);
};

export const postLogin = async (username, password) => {
  let form = new URLSearchParams();
  // get token
  let token = getToken();
  form.append("username", username);
  form.append("password", password);
  form.append("submit", "Log in");
  form.append("next", "");
  form.append("csrfmiddlewaretoken", await token);
  return await $fetch("/api/login/", {
    method: "POST",
    body: form,
    onResponse({ response }) {
      if (response.status == 200) window.location.reload();
    },
  });
};

export const checkIfLoggedIn = async () => {
  $fetch("/api/login", {
    onResponse({ response }) {
      if (response.status == 200) navigateTo("/");
    },
  });
};

export const logout = async () => {
  const resp = await ownUseFetch("/api/auth/logout");
  if (resp.status.value == "success") navigateTo("/login");
};
