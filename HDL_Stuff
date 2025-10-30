30/10/2025 вот собираю тут память из курса нанд2тетрис
## clock
```HDL
/*
* На вход подается 16-битное число period и флаг сброса часов reset.

* У чипа два выхода:
* 1. ticks (0 ≤ ticks < period) — сколько тиков прошло с начала периода,
* 2. loop — равен единице, когда ticks равен нулю.
* 
* Если предыдущее значение ticks оказывается за пределами корректных 
* значений (из-за уменьшения period), нужно вернуть ticks=0, loop=1
*/
CHIP Clock {
    IN period[16], reset;
    OUT ticks[16], loop;

    PARTS:
    // Увеличиваем текущий тик на 1 для следующего шага (счётчик)
    Inc16(in=curtick, out=inctick);
    
    // Вычисляем отрицательное значение увеличенного тика (для вычитания)(not(t)-1=-t)
    Not16(in=inctick, out=netick); 
    
    // Сравниваем: inctick >= period ? 
    // Делаем period - inctick = period + (-inctick) = period + netick
    // Если результат отрицательный (бит знака = 1), значит inctick >= period
    Add16(a=period, b=netick, out=tickdiff, out[15]=tickBiggerPeriod);
    
    // Инвертируем результат сравнения: теперь tickSmallPeriod = 1, если inctick < period
    Not(in=tickBiggerPeriod, out=tickSmallPeriod);
    
    // Проверяем, что НЕ сброс (reset = 0)
    Not(in=reset, out=notReset);
    
    // Разрешаем увеличение, только если НЕ сброс И следующий тик < period
    // doInc = 1 означает "можно увеличить счетчик"
    And(a=notReset, b=tickSmallPeriod, out=doInc);
    
    // Если doInc=1, то берем увеличенное значение inctick, иначе 0
    // То есть либо увеличиваем счетчик, либо сбрасываем в 0
    Mux16(a=false, b=inctick, sel=doInc, out=updatedTicks);
    
    // Отслеживаем переполнение: если tickBiggerPeriod=1, значит был сброс периода
    DFF(in=tickBiggerPeriod, out=tickOverflow);
    
    // Запоминаем предыдущее состояние сброса
    DFF(in=reset, out=previousReset);
    
    // loop=1, если было переполнение ИЛИ активен сброс
    // То есть сигнал "начало нового периода"
    Or(a=tickOverflow, b=previousReset, out=loop);
    
    // Регистр хранит текущее значение тиков и выдает его на выход
    // load=true означает, что регистр всегда обновляется
    Register(in=updatedTicks, load=true, out=ticks, out=curtick);
}
