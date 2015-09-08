import unittest, json, sys, logging
from request.manager import TaskRequest
from manager import kernelMgr
from modules.configuration import MERRA_TEST_VARIABLES
from modules.utilities import wpsLog
wpsLog.addHandler( logging.StreamHandler(sys.stdout) )
wpsLog.setLevel(logging.DEBUG)

class KernelTests(unittest.TestCase):

    def setUp(self):
        self.test_point = [ -137.0, 35.0, 85000 ]
        self.test_time = '2010-01-16T12:00:00'
        self.operations = [ "time.departures(v0,t)", "time.climatology(v0,t,annualcycle)", "time.value(v0)" ]
        self.def_task_args =  { 'region': self.getRegion(), 'data': self.getData() }

    def tearDown(self):
        pass

    def getRegion(self):
        return '{"longitude": %.2f, "latitude": %.2f, "level": %.2f, "time":"%s" }' % (self.test_point[0],self.test_point[1],self.test_point[2],self.test_time)

    def getData(self, vars=[0]):
        var_list = ','.join( [ ( '"v%d:%s"' % ( ivar, MERRA_TEST_VARIABLES["vars"][ivar] ) ) for ivar in vars ] )
        data = '{"%s":[%s]}' % ( MERRA_TEST_VARIABLES["collection"], var_list )
        return data

    def getOp(self, op_index ):
        return [ self.operations[ op_index ] ]

    def getResultData(self, result_data ):
        if "error" in result_data:
            print>>sys.stderr, result_data["error"]
        return result_data.get('data',[])

    def getTaskArgs(self, op ):
        task_args = dict( self.def_task_args )
        task_args['operation'] = op
        return task_args

    def test01_cache(self):
        cache_level = 85000.0
        result = kernelMgr.run( TaskRequest( request={ 'region': { "level": cache_level }, 'data': self.getData() } ) )
        result_stats = result[0]['result']
        self.assertEqual( json.loads(result_stats['region']), { "lev": [cache_level] } )

    def test02_departures(self):
        test_result = [-1.4053638599537024,  -1.2588794849537024, 0.8407298900462976, 2.8915111400462976, -18.592863859953702, -11.854582609953702, -3.2120044849537024, -5.311613859953702, 5.332917390046298, -1.6983326099537024]
        task_args = self.getTaskArgs( op=self.getOp( 0 ) )
        result = kernelMgr.run( TaskRequest( request=task_args ) )
        result_data = self.getResultData(result[0])
        self.assertEqual( test_result, result_data[0:len(test_result)] )

    def test03_annual_cycle(self):
        test_result = [48.07984754774306, 49.218166775173614, 49.36114501953125, 46.40715196397569, 46.3406982421875, 44.37486775716146, 46.54383680555556, 48.780619303385414, 46.378028021918404, 46.693325466579864, 48.840003119574654, 46.627953423394096]
        task_args = self.getTaskArgs( op=self.getOp( 1 ) )
        kernelMgr.persist('all')
        result = kernelMgr.run( TaskRequest( request=task_args ) )
        result_data = self.getResultData(result[0])
        self.assertEqual( test_result, result_data[0:len(test_result)] )

    def test04_value_retreval(self):
        test_result = 59.765625
        task_args = self.getTaskArgs( op=self.getOp( 2 ) )
        result = kernelMgr.run( TaskRequest( request=task_args ) )
        result_data = self.getResultData(result[0])
        self.assertEqual( test_result, result_data )

    def test05_multitask(self):
        test_results = [ [ -1.4053638599537024,  -1.2588794849537024, 0.8407298900462976 ], [48.07984754774306, 49.218166775173614, 49.36114501953125], 59.765625 ]
        task_args = self.getTaskArgs( op=self.operations )
        results = kernelMgr.run( TaskRequest( request=task_args ) )
        for ir, result in enumerate(results):
            result_data = self.getResultData(result)
            test_result = test_results[ir]
            if hasattr( test_result, '__iter__' ):  self.assertEqual( test_result, result_data[0:len(test_result)] )
            else:                                   self.assertEqual( test_result, result_data )