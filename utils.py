import tensorflow as tf
import yaml

slim = tf.contrib.slim


def _get_init_fn(FLAGS):
    """
    This function is copied from TF slim.

    Returns a function run by the chief worker to warm-start the training.

    Note that the init_fn is only run when initializing the model during the very
    first global step.

    Returns:
      An init function run by the supervisor.
    """
    tf.logging.info('Use pretrained model %s' % FLAGS.loss_model_file)

    exclusions = []
    if FLAGS.checkpoint_exclude_scopes:
        exclusions = [scope.strip()
                      for scope in FLAGS.checkpoint_exclude_scopes.split(',')]

    variables_to_restore = []
    for var in slim.get_model_variables():
        excluded = False
        for exclusion in exclusions:
            if var.op.name.startswith(exclusion):
                excluded = True
                break
        if not excluded:
            variables_to_restore.append(var)

    return slim.assign_from_checkpoint_fn(
        FLAGS.loss_model_file,
        variables_to_restore,
        ignore_missing_vars=True)


class Flag(object):
    def __init__(self, **entries):
        self.__dict__.update(entries)


def read_conf_file(conf_file):
    with open(conf_file) as f:
        FLAGS = Flag(**yaml.load(f,Loader=yaml.FullLoader))
    return FLAGS


if __name__ == '__main__':
    f = read_conf_file('conf/mosaic.yml')
    print(f.loss_model_file)
