export const useMealsStore = defineStore("meals", () => {
  const today = ref(new Date())
  const datePicker = ref(new Date());
  const date = computed(() => toDateString(datePicker.value));
  const meals = getMeals(date);

  const checkDate = () => {
    const newDate = new Date()
    if (today.value.getDate() != newDate.getDate()){
      datePicker.value = newDate
    }
  }

  const jumpdays = async (offset) => {
    datePicker.value = new Date(new Date().setDate(datePicker.value.getDate()+offset))
  }
  
  return { ...meals, date, datePicker, today, checkDate, jumpdays };
});
export const usePetsStore = defineStore("pets", () => getPets());
export const useFoodsStore = defineStore("foods", () => {
  const foods = getFoods();
  const last2 = computed(() => {
    return [...foods.data.value.results]
            .sort((a, b) => b.last_used - a.last_used)
            .filter((food) => food.category == 'W')
            .slice(0, 2)
            .sort((a, b) => a.id - b.id)
  });
  const map = computed(() => {
    return Object.entries(foods.data.value.results).reduce((obj, [key, value]) => {
      obj[value.id] = value;
      return obj;
    }, {});
  });
  return { ...foods, map, last2 };
});
export const useSchedulesStore = defineStore("schedules", () => getSchedules());
export const useHelperStore = defineStore("helper", () => getHelper());
export const useFoodOptionsStore = defineStore("foodOptions", () =>
  getFoodOptions()
);