export const ownClone = (ref) => {
  if (!ref.value) return null;
  return structuredClone(toRaw(ref.value.results));
}

export const listToMap = (list) => {
  return Object.entries(list.value).reduce((obj, [key, value]) => {
    obj[value.id] = value;
    return obj;
  }, {});
}

export const useMealsStore = defineStore("meals", () => {
  const today = ref(new Date())
  const datePicker = ref(new Date());
  const date = computed(() => toDateString(datePicker.value));
  const meals = getMeals(date);
  const foods = useFoodsStore();
  // insert food at meal.food
  const list = computed(() => {
    const list = ownClone(meals.data);
    for (const meal of list) {
      meal.food = foods.map[meal.food];
    }
    return list;
  });

  const checkDate = () => {
    const newDate = new Date()
    if (today.value.getDate() != newDate.getDate()){
      datePicker.value = newDate
    }
  }

  const jumpdays = async (offset) => {
    datePicker.value = new Date(new Date().setDate(datePicker.value.getDate()+offset))
  }
  
  return { ...meals, list, date, datePicker, today, checkDate, jumpdays };
});
export const usePetsStore = defineStore("pets", () => {
  const pets = getPets()
  const list = computed(() => ownClone(pets.data));
  return {...pets, list};
});
export const useFoodsStore = defineStore("foods", () => {
  const foods = getFoods();
  const list = computed(() => ownClone(foods.data));
  const last2 = computed(() => {
    return [...list.value]
            .sort((a, b) => b.last_used - a.last_used)
            .filter((food) => food.active && food.category == 'W')
            .slice(0, 2)
            .sort((a, b) => a.id - b.id)
  });
  const map = computed(() => listToMap(list));
  return {...foods, list, map, last2};
});
export const useSchedulesStore = defineStore("schedules", () => {
  const schedules = getSchedules()
  const list = computed(() => ownClone(schedules.data));
  return {...schedules, list};
});
export const useHelperStore = defineStore("helper", () => getHelper());
export const useFoodOptionsStore = defineStore("foodOptions", () =>
  getFoodOptions()
);