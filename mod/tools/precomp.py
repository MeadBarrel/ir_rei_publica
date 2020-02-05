import argparse
import jinja2
import sys
import os


def get_templates_folder(type_):
    return os.path.join('./', 'templates', type_)


def process(type_, parameters):
    jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(get_templates_folder(type_)))
    for template in jinja_env.list_templates():
        raw = jinja_env.get_template(template)
        result = raw.render(**parameters)
        output_name = template
        for key, value in parameters.items():
            output_name = output_name.replace('{%s}' % key, value)
        output_file_path = os.path.join('./output', output_name)
        os.makedirs(os.path.dirname(output_file_path), exist_ok=True)
        with open(output_file_path, 'w', encoding='utf-8-sig') as f:
            f.write(result)



def process_voting(matter, **kwargs):
    process('voting', {'MATTER': matter})



def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()
    voting = subparsers.add_parser('voting')
    voting.add_argument('matter')
    voting.set_defaults(func=process_voting)
    args = parser.parse_args()
    kwargs = vars(args)
    func = kwargs.pop('func', None)
    if func is None:
        parser.print_usage()
        sys.exit(1)
    func(**kwargs)



if __name__ == '__main__':
    main()