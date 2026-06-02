# EXIF Metadata Analyser (Project 013)

A lightweight forensic tool designed to extract hidden metadata from
image files.

## Technical Explanation

-   **Metadata Parsing:** Uses the *Pillow* library to access the EXIF
    directory within image headers.
-   **Tag Translation:** Maps numeric EXIF IDs to human-readable labels
    using *PIL.ExifTags*.
-   **Robust Error Handling:** Safely handles non-text binary data,
    preventing crashes when reading corrupted or obfuscated metadata.

## Problems Solved

1.  **Device Attribution:** Identify the hardware (make/model) used to
    create a file.
2.  **Timeline Analysis:** Extract the precise date and time a photo was
    taken, regardless of the file\'s \"creation date\" on the OS.
3.  **Location Discovery:** Retrieve embedded GPS coordinates to trace
    the physical origin of the image.

## Design Decisions: \"Why this instead of that?\"

  ----------------- ------------------ ------------------------------------------------------------------------------------------------
  **Parsing**       *PIL.ExifTags*     Provides a standardized, fast way to resolve EXIF keys.
  **Safety**        *with* statement   Guarantees that file handles are released correctly, a best practice in forensic environments.
  **Readability**   f-strings          Uses formatted alignment (*:\<20*) to create professional, column-based console output.
  ----------------- ------------------ ------------------------------------------------------------------------------------------------
