document.getElementById('parseButton').addEventListener('click', parseAndCreateICS);

function parseSchedule(scheduleText) {
    const lines = scheduleText.split('\n');
    const shifts = [];
    let currentYear, currentMonth, currentDay;
    let tempShift = {};

    lines.forEach((line, i) => {
        const monthYearMatch = line.match(/(\w+)\s+(\d{4})/);
        if (monthYearMatch) {
            currentMonth = new Date(Date.parse(`${monthYearMatch[1]} 1, 2000`)).getMonth() + 1;
            currentYear = parseInt(monthYearMatch[2], 10);
        }

        const dayMatch = line.match(/(Sunday|Monday|Tuesday|Wednesday|Thursday|Friday|Saturday), (\w+) (\d+)/);
        if (dayMatch) {
            currentDay = parseInt(dayMatch[3], 10);
            const month = new Date(Date.parse(`${dayMatch[2]} 1, 2000`)).getMonth() + 1;
            if (month !== currentMonth) {
                currentMonth = month;
                if (currentMonth === 1 && currentYear) {
                    currentYear += 1;
                }
            }
        }

        const timeMatch = line.match(/(\d{2}):(\d{2})(AM|PM)/);
        if (timeMatch) {
            let hour = parseInt(timeMatch[1], 10);
            const minute = parseInt(timeMatch[2], 10);
            const amPm = timeMatch[3];
            if (amPm === 'PM' && hour !== 12) {
                hour += 12;
            } else if (amPm === 'AM' && hour === 12) {
                hour = 0;
            }
            const shiftTime = { hour, minute };

            if (!tempShift.start_time) {
                tempShift = {
                    date: new Date(currentYear, currentMonth - 1, currentDay),
                    start_time: shiftTime,
                };
            } else {
                tempShift.end_time = shiftTime;
                const startDateTime = new Date(currentYear, currentMonth - 1, currentDay, tempShift.start_time.hour, tempShift.start_time.minute);
                const endDateTime = new Date(currentYear, currentMonth - 1, currentDay, shiftTime.hour, shiftTime.minute);
                if (endDateTime <= startDateTime) {
                    endDateTime.setDate(endDateTime.getDate() + 1);
                }
                tempShift.duration = (endDateTime - startDateTime) / 1000 / 60 / 60; // duration in hours

                let role = 'Unknown';
                for (let j = i; j < i + 5 && j < lines.length; j++) {
                    if (['Starbucks', 'Checkout Advocate'].includes(lines[j].trim())) {
                        role = lines[j].trim();
                        break;
                    }
                }
                tempShift.role = role;
                shifts.push(tempShift);
                tempShift = {};
            }
        }
    });
    return shifts;
}

function createICSFile(shifts) {
    let cal = 'BEGIN:VCALENDAR\nVERSION:2.0\nPRODID:-//hacksw/handcal//NONSGML v1.0//EN\n';
    shifts.forEach(shift => {
        let event = 'BEGIN:VEVENT\n';
        event += `DTSTART:${formatICSDate(shift.date, shift.start_time)}\n`;
        event += `DTEND:${formatICSDate(shift.date, shift.end_time)}\n`;
        event += `SUMMARY:Shift - ${shift.role}\n`;
        event += `DESCRIPTION:Role: ${shift.role}\nDuration: ${shift.duration.toFixed(2)} hrs\n`;
        event += 'END:VEVENT\n';
        cal += event;
    });
    cal += 'END:VCALENDAR';
    return cal;
}

function formatICSDate(date, time) {
    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const day = String(date.getDate()).padStart(2, '0');
    const hour = String(time.hour).padStart(2, '0');
    const minute = String(time.minute).padStart(2, '0');
    return `${year}${month}${day}T${hour}${minute}00`;
}

function downloadICSFile(content, filename) {
    const blob = new Blob([content], { type: 'text/calendar' });
    const link = document.createElement('a');
    link.href = URL.createObjectURL(blob);
    link.download = filename;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
}

function parseAndCreateICS() {
    const scheduleText = document.getElementById('scheduleText').value;
    const parsedShifts = parseSchedule(scheduleText);

    const result = document.getElementById('result');
    if (parsedShifts.length === 0) {
        result.innerHTML = 'No shifts found. Please check your input.';
        document.getElementById('links').classList.add('hidden');
        return;
    }

    let resultText = '<b>Parsed shifts:</b><br>';
    parsedShifts.forEach(shift => {
        resultText += `<p><b>Date:</b> ${shift.date.toDateString()}, <b>Start:</b> ${String(shift.start_time.hour).padStart(2, '0')}:${String(shift.start_time.minute).padStart(2, '0')}, <b>End:</b> ${String(shift.end_time.hour).padStart(2, '0')}:${String(shift.end_time.minute).padStart(2, '0')}, <b>Role:</b> ${shift.role}, <b>Duration:</b> (${shift.duration.toFixed(2)} hrs)</p>`;
    });

    result.innerHTML = resultText;

    const icsContent = createICSFile(parsedShifts);
    const startDate = parsedShifts[0].date;
    const endDate = parsedShifts[parsedShifts.length - 1].date;
    const filename = `work_schedule_${formatDate(startDate)}-${formatDate(endDate)}.ics`;

    downloadICSFile(icsContent, filename);

    document.getElementById('links').classList.remove('hidden');
}

function formatDate(date) {
    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const day = String(date.getDate()).padStart(2, '0');
    return `${year}${month}${day}`;
}
