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

export const dateFormat = (date) => {
    const day = date.getDate();
    const month = date.getMonth() + 1;
    const year = date.getFullYear();
  
    return `Geboren am ${day}.${month}.${year}`;
}

export const getAge = (date) => {
    // in format: 2 Jahre 1 Monat
    const today = new Date();
    const birthDate = new Date(date);
    const diff = today - birthDate;
    const age = Math.floor(diff / 31557600000);
    const months = Math.floor((diff % 31557600000) / 2629800000);
    const year_str = `${age} Jahr${age!=1?'e':''} + `
    const month_str = `${months} Monat${months!=1?'e':''}`
    return `${age?year_str:''}${month_str} alt`;
}