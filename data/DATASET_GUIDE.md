# Driver Dataset Guide

## Recommended classes

1. attentive_driver
2. distracted_driver
3. drowsy_driver
4. phone_usage
5. yawning
6. looking_away
7. eating
8. drinking

## Annotation

YOLO format:

```text
class_id center_x center_y width height
```

Example:

```text
3 0.61 0.71 0.20 0.31
```

All coordinates are normalized.

## Train / validation split

Use approximately:

- 80% train
- 20% validation

Keep classes balanced and include different:
- lighting conditions
- camera angles
- drivers
- glasses/no glasses
- clothing
- seating positions

Only use images you have permission to use.
