from modules.utilities import get_json_arg
from modules import configuration
from datacache.manager import dataManager

class KernelManager:

    def run( self, run_args ):
        operation = get_json_arg( 'operation', run_args )
        kernel = self.getKernel( operation )
        if kernel:
            result = kernel.run( run_args )
            return result
        else:
            raise Exception( "No compute kernel found for operation %s" % str(operation) )

    def getKernel( self, operation ):
        if not operation:
            from cda import DataAnalytics
            return DataAnalytics()
        if operation.get('kernel','base') == 'time':
            from timeseries_analysis import TimeseriesAnalytics
            return TimeseriesAnalytics()

    def processOperations( self, operations_spec ):
        op_spec_list = operations_spec.split(';')
        for op_spec in op_spec_list:
            op_spec_toks = op_spec.split('=')
            if len( op_spec_toks ) == 2:
                dataManager.addCachedVariable( op_spec_toks[0].strip(), op_spec_toks[1].strip() )
            else:
                pass # TODO: utility cmds

        result_variables = self.data_cache.getResults()
        results = {}
        for result_variable in result_variables:
            kernel = self.getKernel( result_variable.operation )
            if kernel:
                result = kernel.run( result_variable.operation )
                results[ result_variable.id ] = result
            else:
                raise Exception( "No compute kernel found for operation %s" % str( result_variable.operation ) )
        return results





kernelMgr = KernelManager()
