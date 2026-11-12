
import os
import uuid

renamed = 0
skipped = 0
errors = 0

try:
    BASE_DIR = os.path.dirname(
        os.path.dirname(
            os.path.dirname(os.path.abspath(__file__))
        )
    )

    folder_path = os.path.join(
        BASE_DIR,
        'Interview',
        'programming-languages-aktu'
    )

    if not os.path.isdir(folder_path):
        raise FileNotFoundError("Target folder does not exist.")

    for root, dirs, files in os.walk(folder_path, topdown=False):

        for name in files + dirs:
            new_name = name.lower()

            if name == new_name:
                continue

            old_path = os.path.join(root, name)
            new_path = os.path.join(root, new_name)

            try:
                if os.path.exists(new_path):
                    if os.path.samefile(old_path, new_path):
                        temp_path = os.path.join(
                            root, ".temp-" + uuid.uuid4().hex
                        )

                        os.rename(old_path, temp_path)

                        try:
                            os.rename(temp_path, new_path)
                        except Exception:
                            os.rename(temp_path, old_path)
                            raise
                    else:
                        print("Skipped: Target already exists:", new_path)
                        skipped += 1
                        continue
                else:
                    os.rename(old_path, new_path)

                print(f"Renamed: {name} -> {new_name}")
                renamed += 1

            except PermissionError:
                print("Permission denied:", old_path)
                errors += 1

            except OSError as e:
                print("OS Error:", e)
                errors += 1

            except Exception as e:
                print("Unexpected Error:", e)
                errors += 1

    print("\nRenaming completed.")
    print("Successfully renamed:", renamed)
    print("Skipped:", skipped)
    print("Errors:", errors)

except Exception as e:
    print("Error:", e)
