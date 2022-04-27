/* Based of https://stackoverflow.com/a/36947127 */

UPDATE velages
SET date = substr(date, -4) || '-' || substr('0' || substr(date, 1, instr(date, '/') -1), -2) || '-' || substr('0' || substr(date, instr(date, '/') +1, length(date)-5-instr(date, '/')), -2)
WHERE  substr(date, -5, 1) = '/'
AND date LIKE '%/%/%'
