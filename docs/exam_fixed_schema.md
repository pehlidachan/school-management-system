# Fixed Exam Schema

The ERP now uses a fixed exam frame for school assessment planning.

## Exam types

1. Weekly Test
2. Monthly Test
3. Quarterly Test
4. Mid Term Exam
5. Pre Final Exam
6. Final Exam

## Database models

### Exam

Stores the main exam/assessment schema:

```text
name
exam_type
academic_year
term_label
grade
start_date
end_date
sequence
result_weight
is_locked
is_published
created_by
```

### ExamSubject

Stores subjects inside an exam:

```text
exam
subject
total_marks
passing_marks
```

### ExamDateSheetItem

Stores a real datesheet row for each subject paper:

```text
exam_subject
paper_date
start_time
end_time
room
instructions
sort_order
```

### StudentMark

Stores the marks of each student in each exam subject:

```text
exam_subject
student
marks_obtained
remarks
marked_by
```

## Default sequence and result weight

| Exam type | Sequence | Default result weight |
|---|---:|---:|
| Weekly Test | 10 | 5% |
| Monthly Test | 20 | 10% |
| Quarterly Test | 30 | 15% |
| Mid Term Exam | 40 | 25% |
| Pre Final Exam | 50 | 20% |
| Final Exam | 60 | 25% |

## Lock policy

When an exam is locked:

- Subjects cannot be changed.
- Marks cannot be changed.
- Results remain readable/printable.

## Future DMC use

Final DMC can later combine multiple exam types using `result_weight` to calculate annual weighted score.
