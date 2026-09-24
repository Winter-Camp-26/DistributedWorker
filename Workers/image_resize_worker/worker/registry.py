from jobs.image_resize import resize_image


JOB_HANDLERS = {
    "IMAGE_RESIZE": resize_image,
}


def get_handler(job_type: str):
    """
    Return the handler associated with a job type.
    """

    handler = JOB_HANDLERS.get(job_type)

    if handler is None:
        raise ValueError(
            f"Unsupported job type: {job_type}"
        )

    return handler