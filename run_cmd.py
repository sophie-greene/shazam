import subprocess


def run_cmd(cmd, capture_output=False, capture_error=False):


    # Set up subprocess with stderr and stdout redirection
    args = {}
    if capture_output:
        args["stdout"] = subprocess.PIPE
    if capture_error:
        args["stderr"] = subprocess.PIPE
    # get my current env settings
    if not capture_output and not capture_error:
        subprocess.call(cmd)
        return
    p = subprocess.Popen(cmd.split(" "), **args)

    # Capture output and error streams
    out, err = p.communicate()

    # If both output and error streams are requested
    if capture_output and capture_error:
        if out and err:
            return out.splitlines(), err.splitlines()
    if out and not err:
        return out.splitlines()
    if not out and err:
        err.splitlines()
    # If only output stream is requested
    elif capture_output:
        return out.splitlines() if out else []

    # If only error stream is requested
    elif capture_error:
        return err.splitlines() if err else []
