
from model.models import *
from edit_parts.edit_parts import *


class CommandManager():
	def __init__(self, scene_edit_part):
		self.scene_edit_part = scene_edit_part

	def execute(self, command):
		command.scene_edit_part = self.scene_edit_part
		command.execute()

class Command():
	def __init__(self):
		self.scene_edit_part = None

class AddToQueueTransactionCommand(Command):
	def __init__(self, ins, count_outs):
		self.ins = ins
		self.count_outs = count_outs
		self.scene_edit_part = None

	def execute(self):
		TransactionEditPart.addNewTransactionToQueue(self.scene_edit_part, self.ins, self.count_outs)

class LoadNextTransactionToValidatorCommand(Command):
	def __init__(self):
		self.scene = None
	def execute(self):
		self.scene_edit_part.validator_edit_part.loadNextTransaction()

class ValidateTransactionCommand(Command):
	def __init__(self):
		self.scene = None
	def execute(self):
		self.scene_edit_part.validator_edit_part.validateTransaction()


class ValidatorDispatchTxCommand(Command):
	def __init__(self):
		self.scene = None
	def execute(self):
		self.scene_edit_part.validator_edit_part.dispatch()


class AddBlockToChainCommand(Command):
	def __init__(self):
		self.scene = None
	def execute(self):
		self.scene_edit_part.preparing_block_edit_part.loadBlock()


class UpdateLivingViewCommand(Command):
	def __init__(self):
		self.scene = None
	def execute(self):
		self.scene_edit_part.model.living_board.update()

class UpdateLimboCommand(Command):
	def __init__(self):
		self.scene = None
	def execute(self):
		self.scene_edit_part.model.limbo.update()

class ChangeTxDisplayModeCommand(Command):
	def __init__(self):
		self.scene = None
	def execute(self):
		self.scene_edit_part.changeTxDisplayMode()





