
import threading
import subprocess
import time

def get_row(outfile):
    """
    The get_row function runs the shazam_step shortcut
    and returns a subprocess.CompletedProcess object.
    Please refer to the documentation for subprocess.
    
    :param outfile: Specify the path for the output file
    :return: A CompletedProcess object
    """
    script = ["shortcuts",
              "run",
              "shazam_step",
              "--output-path",
              outfile]
    return subprocess.run(script, capture_output=True, text=True, check=False)
def run_get_row(outfile):
  # Global variable to signal thread termination
  terminate_flag = False

  # Function to perform critical task
  def critical_task():
      try:
          while not terminate_flag:
              # Simulate a critical task
              print("Critical task running")
              time.sleep(.1)
      except KeyboardInterrupt:
          print("Keyboard interrupt received")

  # Function to handle cleanup tasks
  def cleanup():
      nonlocal terminate_flag
      # print("Cleaning up resources...")
      # Set the termination flag to True to signal thread termination
      terminate_flag = True

  # Create a new thread for get_row function
  thr_get_row = threading.Thread(target=get_row, args=(outfile,))

  # Start the thread for get_row function
  thr_get_row.start()

  # Create a new thread for the critical task
  th_monitor_get_row = threading.Thread(target=critical_task)

  # Start the critical thread
  th_monitor_get_row.start()

  try:
      # Main thread will continue running until interrupted
      while True:
          time.sleep(1)
  except KeyboardInterrupt:
      # Handle keyboard interrupt
      print("Main thread received keyboard interrupt")
      # Perform cleanup tasks
      cleanup()
      # Wait for the get_row thread to finish
      thr_get_row.join()
      # Wait for the critical thread to finish
      th_monitor_get_row.join()

  # Main thread exiting
  print("Get_row clean-up ends here")

run_get_row('./x.txt')