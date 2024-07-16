import time
import serial
import subprocess
from serial.tools import list_ports

def get_com_ports():
    return set([port.device for port in list_ports.comports()])

def toggle_com_port(com_port):
    try:
        # Get the list of COM ports before reopening
        initial_ports = get_com_ports()

        # Open the COM port
        ser = serial.Serial(com_port)
        print(f"Opened {com_port} successfully.")
        
        # Close the COM port
        ser.close()
        print(f"Closed {com_port}.")

        # Delay for 500 ms
        time.sleep(0.5)

        # Reopen the COM port at 1200 baud rate
        ser = serial.Serial(com_port, baudrate=1200)
        print(f"Reopened {com_port} at 1200 baud rate.")
        
        # Close the COM port after reopening
        ser.close()
        print(f"Closed {com_port} after reopening.")

        # Delay for the new COM port to appear
        time.sleep(2)

        # Get the list of COM ports after reopening
        new_ports = get_com_ports()
        new_com_port = (new_ports - initial_ports).pop()
        print(f"Detected new COM port: {new_com_port}")

        # Upload the firmware using the new COM port
        upload_firmware(new_com_port)
        
    except serial.SerialException as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def upload_firmware(new_com_port):
    try:
        # Command to upload firmware using adafruit-nrfutil
        command = [
            "adafruit-nrfutil.exe",
            "dfu",
            "serial",
            "-p", new_com_port,
            "-b", "115200",
            "--singlebank",
            "-pkg", "firmware.zip"
        ]
        
        # Run the command and capture real-time output
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        # Display the output line by line
        while True:
            output = process.stdout.readline()
            if output == '' and process.poll() is not None:
                break
            if output:
                print(output.strip())

        # Get the return code and check if the command was successful
        return_code = process.poll()
        if return_code == 0:
            print("Firmware uploaded successfully.")
        else:
            print(f"Failed to upload firmware with return code {return_code}.")
            error_output = process.stderr.read()
            print(error_output.strip())

        # Delay for 10 seconds
        print("Waiting for 10 seconds...")
        time.sleep(10)
        print("Done waiting.")

    except Exception as e:
        print(f"An error occurred while uploading firmware: {e}")

if __name__ == "__main__":
    # Prompt the user for the COM port
    com_port = input("Enter the COM port (e.g., COM3): ")
    
    toggle_com_port(com_port)
