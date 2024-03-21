class NonPosDiskNumError(Exception):
    """Error class for non positive number of disks"""
    pass


class InvalidAutoSolveError(Exception):
    """Error class for invalid auto solve command"""
    pass


class InvalidMoveError(Exception):
    """Error class for invalid move command"""
    pass


class Hanoi:
    """Class for Tower of Hanoi

    Attributes
    ----------
    stacks : list
        list of 3 stacks
    num_of_disks : total number of disks
    """

    stacks = []

    def __init__(self, num_of_disks: int):

        """Constructor for initializing Hanoi instance
        :param num_of_disks: initial number of disks on stack 0, must be > 0
        :type num_of_disks: int
        :raise NonPosDiskNum: raises error if given non positive num_of_disks
        """

        if num_of_disks < 1:
            raise NonPosDiskNumError('Non positive disk number')

        self.num_of_disks = num_of_disks
        self.stacks.append(list(range(num_of_disks, 0, -1)))
        self.stacks.append([])
        self.stacks.append([])

    def print_stacks(self):
        """Method to print out all 3 stacks

        """
        for i in range(3):
            print('Stack ' + str(i) + ':', end=' ')
            print(self.stacks[i], end=' ')
        print()

    def move(self, start: int, to: int):

        """Method to move disk from 'start' stack to 'to' stack

        :param start: 'start' stack, must be >= 0 and <= 2
        :type start: int
        :param to: 'to' stack, must be >= 0 and <= 2
        :type to: int
        :raise InvalidMoveError: raises error if either stack is < 0 or > 2 or if 'start' stack has no disks
            or if move was for a larger disk onto a smaller disk
        """

        if start < 0 or start > 2 or to < 0 or to > 2:
            raise InvalidMoveError('Please ensure moves are from a stack 0-2 to another stack 0-2.')

        if len(self.stacks[start]) < 1:
            raise InvalidMoveError('Please ensure moves come from a stack with at least one disk.')

        if self.stacks[to] and self.stacks[to][-1] < self.stacks[start][-1]:
            raise InvalidMoveError('Please ensure moves move smaller disk onto a larger disk.')
            
        self.stacks[to].append(self.stacks[start].pop())

    def solve(self, num_of_above_disks, start, to):

        """Method to auto solve tower

        :param num_of_above_disks: number of disks above bottom disk at 'start' stack
        :type num_of_above_disks: int
        :param start: 'start' stack
        :type start: int
        :param to: 'to' stack
        :type to: int
        """

        if num_of_above_disks == self.num_of_disks-1:
            if len(self.stacks[1]) > 0 or len(self.stacks[2]) > 0:
                raise InvalidAutoSolveError('All disks must be on stack 0')

        if num_of_above_disks == 0:
            self.move(start, to)
            self.print_stacks()
        else:
            self.solve(num_of_above_disks-1, start, 3-start-to)
            self.move(start, to)
            self.print_stacks()
            self.solve(num_of_above_disks-1, 3-start-to, to)

    def reset(self):
        """Method to reset stacks to original configuration

        """
        self.stacks.clear()
        self.stacks.append(list(range(self.num_of_disks, 0, -1)))
        self.stacks.append([])
        self.stacks.append([])


def main():
    """ Main method, handles user input

    """
    user_disk_num = 0
    tower = 0

    # user input num of disks
    while user_disk_num < 1:
        try:
            user_disk_num = int(input('How many disks would you like? '))
            tower = Hanoi(user_disk_num)
        except ValueError:
            print('Please enter an integer number of disks. ')
        except NonPosDiskNumError:
            print('Please enter a positive number of disks. ')

    tower.print_stacks()

    # user commands
    while True:
        user_cmd = input('Please enter a valid command. ')
        # reset stacks
        if user_cmd == 'r':
            tower.reset()
        # quit program
        elif user_cmd == 'q':
            exit(0)
        # auto solve
        elif user_cmd == 'a':
            try:
                tower.solve(user_disk_num - 1, 0, 2)
            except InvalidAutoSolveError:
                print('To use auto solve, please place all disks on stack 0.')
        # print stacks
        elif user_cmd == 'p':
            tower.print_stacks()
        # move disks
        elif len(user_cmd.split(' ')) == 2 and \
                user_cmd.split(' ')[0].isnumeric() and user_cmd.split(' ')[1].isnumeric():
            try:
                tower.move(int(user_cmd.split(' ')[0]), int(user_cmd.split(' ')[1]))
            except InvalidMoveError as e:
                print(e)


if __name__ == '__main__':
    main()
