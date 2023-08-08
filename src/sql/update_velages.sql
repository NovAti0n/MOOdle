/* This Source Form is subject to the terms of the MOOdle OOpen Dairy LicensE, v. 1.0. */
/* Copyright (c) 2022 Noa Quenon */

/* Based of https://www.b4x.com/android/forum/threads/solved-change-date-format-dd-mm-yyyy-to-yyyy-mm-dd-in-sqlite.75309/post-478118 */

UPDATE velages SET date = substr(date, 7, 4) || '-' || substr(date, 4, 2) || '-' || substr(date, 1, 2)
