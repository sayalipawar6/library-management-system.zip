# Project Statement

## Problem Statement

Many small libraries, school reading rooms, and departments still keep track of their book inventory and student check-outs using physical register books or simple excel sheets. This manual method makes it slow, disorganized, and easy to make mistakes when checking basic things like: Is a specific book available on the shelf right now? Which books are past their return date? Who borrowed a particular item? 

Because there is no centralized database system, data can easily be entered wrong or lost, and searching the inventory manually takes too long. A lightweight, simple web application is needed to make day-to-day library tracking digital, accurate, and easy to search.

## Scope of the Project

This project focuses on creating a web application for a single librarian to manage the book database and track lending activities from start to finish. It handles:

•⁠  ⁠Secure librarian account registration and login pages.
•⁠  ⁠Adding new book records, editing details, removing items, and searching the database.
•⁠  ⁠Issuing a book copy to a student and calculating its return due date.
•⁠  ⁠Processing the return of a borrowed book copy to update inventory counts.
•⁠  ⁠A live dashboard summarizing total books, available stock, current loans, and listing overdue entries.

What is not included in this project submission: Separate student self-service login panels, fee/fine calculations for late returns, automated email notifications, or managing multiple library branches. These are left as potential ideas for future updates.

## Target Users

•⁠  ⁠*Librarians and Library Staff:* Who need an easy digital interface to handle book check-outs and check-ins without sorting through paper logs.
•⁠  ⁠*Small Institutions:* Such as school libraries, departmental reading rooms, or local community centers that have outgrown excel spreadsheets but do not need large, expensive commercial library systems.

## Main System Features

1.⁠ ⁠Librarian signup and login system using secure hashed passwords and temporary browser sessions.
2.⁠ ⁠Complete book catalog management (including adding, editing, deleting, and text searches).
3.⁠ ⁠Lending management workflow (automatically assigns a 14-day borrowing window, processes book returns, and blocks check-outs if a book has 0 copies available).
4.⁠ ⁠Status dashboard (displays total books on hand, available copies, active loans, and a list of overdue entries).
5.⁠ ⁠Input checking to prevent blank forms or negative numbers, along with clear notification banners for errors.
