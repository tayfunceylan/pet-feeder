export const useMealsStore = defineStore("meals", () => {
  const datePicker = ref(new Date());
  const date = computed(() => toDateString(datePicker.value));
  const meals = getMeals(date);
  
  return { ...meals, date, datePicker };
});
export const usePetsStore = defineStore("pets", () => getPets());
export const useFoodsStore = defineStore("foods", () => getFoods());
export const useSchedulesStore = defineStore("schedules", () => getSchedules());
export const useHelperStore = defineStore("helper", () => getHelper());
export const useFoodOptionsStore = defineStore("foodOptions", () =>
  getFoodOptions()
);