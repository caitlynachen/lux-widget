import lux
from lux.interestingness.interestingness import interestingness
from lux.compiler.Compiler import Compiler
from lux.executor.PandasExecutor import PandasExecutor
'''
Shows possible visualizations when an additional attribute is added to the current view
'''
def enhance(ldf):
	recommendation = {"action":"Enhance",
					"description":"Shows possible visualizations when an additional attribute is added to the current view."}
	output = []
	# Collect variables that already exist in the context
	context = ldf.getAttrsSpecs()
	# context = [spec for spec in context if isinstance(spec.attribute,str)]
	existingVars = [spec.attribute for spec in context]
	# if we too many column attributes, return no views.
	if(len(context)>2):
		recommendation["collection"] = []
		return recommendation

	# First loop through all variables to create new view collection
	for qVar in ldf.columns:
		if qVar not in existingVars and ldf.dataTypeLookup[qVar] != "temporal":
			cxtNew = context.copy()
			cxtNew.append(lux.Spec(attribute = qVar))
			view = lux.view.View.View(cxtNew)
			output.append(view)
	vc = lux.view.ViewCollection.ViewCollection(output)
	vc = Compiler.compile(ldf,vc,enumerateCollection=False)
	PandasExecutor.execute(vc,ldf)
	# Then use the data populated in the view collection to compute score
	for view in vc:
		# TODO (Jaywoo): fix interestingness function
		view.score = 0.5 #interestingness(tempDataObj)
		output.append(view)
		# TODO: if (ldf.dataset.cardinality[cVar]>10): score is -1. add in interestingness
	vc.sort(removeInvalid=True)
	recommendation["collection"] = vc
	return recommendation