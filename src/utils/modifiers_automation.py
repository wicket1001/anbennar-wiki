#!/bin/python3
import csv
import subprocess
from subprocess import PIPE
import os
import sys


def get_line_for_input():
    os.environ['RUSTC_BOOTSTRAP'] = '1'

    command = '/usr/bin/cargo test --color=always --package anbennar-wiki --bin anbennar-wiki bundled_modifiers::tests::test_triggered_modifiers_parse --no-fail-fast -- --format=json --exact -Z unstable-options --show-output'

    result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=PIPE)
    if result.returncode == 0:
        print("The bash script was successful.")
        print("YOU CAN SLEEP NOW")
        sys.exit(0)
    else:
        output = result.stdout.decode('UTF-8')
        interest = output.split('UNKNOWN ')
        insert = interest[0][interest[0].rindex('    '):][:-4]
        insert = insert.replace('\\', '')
        mod = interest[1][:interest[1].index('\\n')]
        print(insert)
        print(mod)
        print("The bash script failed.")
        return insert


def insert_line(csv_file, output, where):
    skip = 155
    with open(csv_file, 'r') as f:
        with open(output, 'w') as out:
            i = 0
            found = False
            for line in f:
                i += 1
                if i < skip:
                    out.write(line)
                    continue
                if found:
                    out.write(line)
                    continue
                if line > where:
                    print(line)
                    print(where)
                    out.write(where + '\n')
                    out.write(line)
                    found = True
                    continue
                out.write(line)


def get_changes(csv_file):
    changes = {}
    with open(csv_file, 'r') as f:
        reader1 = csv.reader(f, delimiter=';', quotechar='"')
        print(reader1)
        for line in reader1:
            print(line)
            changes[line[0]] = {'id': line[0], 'false': line[1], 'corrected': line[2]}
    return changes


def change_localisation(csv_file, output, changes):
    skip = 160
    with open(csv_file, 'r') as f:
        with open(output, 'w') as out:
            i = 0
            for line in f:
                i += 1
                if i < skip:
                    out.write(line)
                    continue
                try:
                    value = line[line.index('"') + 1:]
                    value = value[:value.index('"')]
                except ValueError as e:
                    out.write(line)
                    continue
                if value in changes:
                    print(changes[value])
                    outting = line.replace(changes[value]['false'], changes[value]['corrected'])
                    print(line)
                    print(outting)
                    out.write(outting)
                    continue
                out.write(line)


if __name__ == '__main__':
    # while True:
    #     input_line = get_line_for_input()
    #     insert_line('modifiers.rs', 'modifiers2.rs', input_line)
    #     os.rename('modifiers2.rs', 'modifiers.rs')

    changes = get_changes('res/modifier_names.csv')
    change_localisation('modifiers.rs', 'modifiers2.rs', changes)
    os.rename('modifiers2.rs', 'modifiers.rs')
