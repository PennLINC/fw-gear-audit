import flywheel
import logging
import warnings
import argparse
import pprint
import pandas as pd
from tabulate import tabulate


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('Flywheel-Gear-Auditor')


def gather_jobs(sessions_list, verbose):
    '''
    Creates a dataframe summarising the gear jobs that have run on the list of sessions
    '''
    df = pd.DataFrame()
    for sess in sessions_list:

        for al in sess.analyses:

            basic_row = {
                'subject': sess.subject.label,
                'session': sess.label,
                'gear_name': al.gear_info['name'],
                'gear_version': al.gear_info['version'],
                'run_label': al.label,
                'run_datetime': al.job['created'],
                'run_runtime_mins': al.job.profile['elapsed_time_ms'],
                'run_status': al.job.state
            }

            final = pd.DataFrame(basic_row, index=[0])

            if verbose:

                config = al.job.config['config']
                inputs = al.job.inputs
                inputs = {k: v['name'] for k, v in inputs.items()}

                config_cols = pd.DataFrame(list(config.items()), columns=['Config_Option', 'Config_Value'])
                inputs_cols = pd.DataFrame(list(inputs.items()), columns=['Inputs_Option', 'Inputs_Value'])

                final = pd.concat([final, inputs_cols, config_cols], axis=1)

            df = pd.concat([df, final])

    return(df)


def gather_seqInfo(args, verbose):
    '''
    Runs fw-heudiconv-tabulate to attach sequence information to the gear jobs query
    Inputs:
        args --
    '''


    return None


def gather_pipelines(sessions_list, verbose):

    df = pd.DataFrame()
    for sess in sessions_list:

        for al in sess.analyses:

            basic_row = {
                'subject': sess.subject.label,
                'session': sess.label,
                'gear_name': al.gear_info['name'],
                'gear_version': al.gear_info['version'],
                'run_label': al.label,
                'run_datetime': al.job['created'],
                'run_runtime_mins': al.job.profile['elapsed_time_ms'],
                'run_status': al.job.state
            }

            final = pd.DataFrame(basic_row, index=[0])

            if verbose:

                config = al.job.config['config']
                inputs = al.job.inputs
                inputs = {k: v['name'] for k, v in inputs.items()}

                config_cols = pd.DataFrame(list(config.items()), columns=['Config_Option', 'Config_Value'])
                inputs_cols = pd.DataFrame(list(inputs.items()), columns=['Inputs_Option', 'Inputs_Value'])

                final = pd.concat([final, inputs_cols, config_cols], axis=1)

            df = pd.concat([df, final])

    return(df)


def get_sessions(client, project_label, subject_labels=None, session_labels=None):
    """Query the flywheel client for a project name
    This function uses the flywheel API to find the first match of a project
    name. The name must be exact so make sure to type it as is on the
    website/GUI.
    Parameters
    ---------
    client
        The flywheel Client class object.
    project_label
        The name of the project to search for.
    subject_labels
        List of subject IDs
    session_labels
        List of session IDs

    Returns
    ---------
    sessions
        A list of session objects
    """
    logger.info("Querying Flywheel server...")

    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        project_obj = client.projects.find_first('label="{}"'.format(project_label))
        assert project_obj, "Project not found! Maybe check spelling...?"
        logger.debug('Found project: %s (%s)', project_obj['label'], project_obj.id)

    sessions = client.get_project_sessions(project_obj.id)
    # filters
    if subject_labels:
        sessions = [s for s in sessions if s.subject['label'] in subject_labels]
    if session_labels:
        sessions = [s for s in sessions if s.label in session_labels]

    sessions = [client.get(s.id) for s in sessions]
    return sessions


def get_parser():

    parser = argparse.ArgumentParser(
        description="Audit gear runs on Flywheel")
    parser.add_argument(
        "--project",
        help="The project in flywheel",
        nargs="+",
        required=True
    )
    parser.add_argument(
        "--subject",
        help="The subject label(s)",
        nargs="+",
        default=None
    )
    parser.add_argument(
        "--session",
        help="The session label(s)",
        nargs="+",
        default=None
    )
    parser.add_argument(
        "--verbose",
        help="Print ongoing messages of progress",
        action='store_true',
        default=False
    )
    parser.add_argument(
        "--dry_run",
        help="Don't apply changes",
        action='store_true',
        default=False
    )

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "--path",
        help="Path to download output file",
        default=None,
        required=False
    )
    group.add_argument(
        "--fname",
        help="Path & name of output file",
        default=None,
        required=False
    )

    group2 = parser.add_mutually_exclusive_group(required=True)
    group2.add_argument(
        "--by-run",
        help="Audit of every gear that has run in the query",
        default=None,
        required=False
    )
    group2.add_argument(
        "--by-sequence",
        help="Audit of every gear that has run in the query incl. sequence info for filtering (not recommended with --verbose)",
        default=None,
        required=False
    )

    return parser


def main():
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        fw = flywheel.Client()
    assert fw, "Your Flywheel CLI credentials aren't set!"
    parser = get_parser()
    args = parser.parse_args()

    project_label = ' '.join(args.project)

    if args.path:
        path = args.path + "/Gear_Audit.csv"
    else:
        path = args.fname

    sessions = get_sessions(client=fw,
                    project_label=project_label,
                    session_labels=args.session,
                    subject_labels=args.subject)

    if args.by_run:

        gear_df = gather_jobs(sessions, args.verbose)

        if gear_df.shape == (0, 0):
            logger.info("No gears run for this query!")
        else:

            if args.dry_run:
                logger.info(tabulate(gear_df, headers='keys', tablefmt='psql'))
            else:
                gear_df.to_csv(path, sep=",", index=False)

if __name__ == '__main__':
    main()
