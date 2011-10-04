
#-* -encoding: utf - 8 -* -

import netsvc
import pooler, tools
import math
import tools
from tools.translate import _

from osv import fields, osv

import wizard
import decimal_precision as dp
import time


class variazioni_iva(osv.osv_memory):
   _name = "variazioni.iva"
   _description = "Varia Codici Iva"
   _columns = {
                'old_cod_deb_id':fields.many2one('account.tax', 'Vecchio Codice Iva a Debito', required=False, readonly=False),
                'new_cod_deb_id':fields.many2one('account.tax', 'Nuovo Codice Iva a Debito', required=False, readonly=False),
                'old_cod_cre_id':fields.many2one('account.tax', 'Vecchio Codice Iva a Credito', required=False, readonly=False),
                'new_cod_cre_id':fields.many2one('account.tax', 'Nuovo Codice Iva a Credito', required=False, readonly=False),
                'flag_base':fields.boolean('Modifica Dati Di Base', required=False),
            }
   
   def varia(self, cr, uid, ids, context):
       param = self.browse(cr, uid, ids)[0]
       if ids:
           ids_art = self.pool.get('product.product').search(cr, uid, [])
           if ids_art:
               param = self.browse(cr, uid, ids)[0]
               riga = {}
               for product in self.pool.get('product.product').browse(cr, uid, ids_art):
                   if param.old_cod_deb_id:
                       lista_tax = []
                       for tax_id in product.taxes_id:
                           if param.old_cod_deb_id.id == tax_id.id:
                               # è da sostituire 
                               lista_tax.append(param.new_cod_deb_id.id)
                           else:
                                lista_tax.append(tax_id.id)
                       riga.update({'taxes_id':[(6, 0, lista_tax)]})
                       
                   if param.old_cod_cre_id:
                       lista_taxs = []
                       # deve verificare se cambiare supplier_taxes_id
                       for sup_tax in product.supplier_taxes_id:
                           if param.old_cod_cre_id.id == sup_tax.id:
                               lista_taxs.append(param.new_cod_cre_id.id)
                           else:
                               lista_taxs.append(sup_tax.id) 
                       riga.update({'supplier_taxes_id':[(6, 0, lista_taxs)]})
                       if riga:
                           ok = self.pool.get('product.product').write(cr, uid, [product.id], riga)
           if param.flag_base:
                #import pdb;pdb.set_trace()
                # va a modificare i dati di base 
                ir_values = self.pool.get('ir.values')
                ir_values.set(cr, uid, key='default', key2=False, name="taxes_id", company=self.pool.get('res.users').browse(cr, uid, uid).company_id.id,
                   models=[('product.product', False)], value=[param.new_cod_deb_id.id])
                ir_values.set(cr, uid, key='default', key2=False, name="supplier_taxes_id", company=self.pool.get('res.users').browse(cr, uid, uid).company_id.id,
                    models=[('product.product', False)], value=[param.new_cod_cre_id.id])
                       
                           
       return{}
variazioni_iva()


class var_dati_art(osv.osv):
   
   _name = "var.dati_art"
   _description = "Varia Codici Iva"
   _columns = {
                'old_cod_deb_id':fields.many2one('account.tax', 'Vecchio Codice Iva a Debito', required=False, readonly=False),
                'new_cod_deb_id':fields.many2one('account.tax', 'Nuovo Codice Iva a Debito', required=False, readonly=False),
                'old_cod_cre_id':fields.many2one('account.tax', 'Vecchio Codice Iva a Credito', required=False, readonly=False),
                'new_cod_cre_id':fields.many2one('account.tax', 'Nuovo Codice Iva a Credito', required=False, readonly=False),
                'flag_base':fields.boolean('Modifica Dati Di Base', required=False),
            }
   
   
   def varia(self, cr, uid, ids, context):
       param = self.browse(cr, uid, ids)[0]
       inseriti = 0
       aggiornati = 0
       if ids:
           ids_art = self.pool.get('product.product').search(cr, uid, [])
           if ids_art:
               param = self.browse(cr, uid, ids)[0]
               riga = {}
               for product in self.pool.get('product.product').browse(cr, uid, ids_art):
                   if param.old_cod_deb_id:
                       lista_tax = []
                       for tax_id in product.taxes_id:
                           if param.old_cod_deb_id.id == tax_id.id:
                               # è da sostituire 
                               lista_tax.append(param.new_cod_deb_id.id)
                           else:
                                lista_tax.append(tax_id.id)
                       riga.update({'taxes_id':[(6, 0, lista_tax)]})
                       
                   if param.old_cod_cre_id:
                       lista_taxs = []
                       # deve verificare se cambiare supplier_taxes_id
                       for sup_tax in product.supplier_taxes_id:
                           if param.old_cod_cre_id.id == sup_tax.id:
                               lista_taxs.append(param.new_cod_cre_id.id)
                           else:
                               lista_taxs.append(sup_tax.id) 
                       riga.update({'supplier_taxes_id':[(6, 0, lista_taxs)]})
                       if riga:
                           aggiornati += 1
                           ok = self.pool.get('product.product').write(cr, uid, [product.id], riga)
           if param.flag_base:
                #import pdb;pdb.set_trace()
                # va a modificare i dati di base 
                ir_values = self.pool.get('ir.values')
                ir_values.set(cr, uid, key='default', key2=False, name="taxes_id", company=self.pool.get('res.users').browse(cr, uid, uid).company_id.id,
                   models=[('product.product', False)], value=[param.new_cod_deb_id.id])
                ir_values.set(cr, uid, key='default', key2=False, name="supplier_taxes_id", company=self.pool.get('res.users').browse(cr, uid, uid).company_id.id,
                    models=[('product.product', False)], value=[param.new_cod_cre_id.id])
                       
                           
       return [inseriti, aggiornati]


   def run_auto_var(self, cr, uid, automatic=False, use_new_cursor=False, context=None):
      pool = pooler.get_pool(cr.dbname)  
      #import pdb;pdb.set_trace()
      testo_log = """Inizio procedura di aggiornamento aliquote iva articoli """ + time.ctime() + '\n'
      ids_param = pool.get('var.dati_art').search(cr, uid, [])
      if ids_param:
          res = self.varia(cr, uid, ids_param, context)
          testo_log = testo_log + " Inseriti " + str(res[0]) + " Aggiornati " + str(res[1]) + " Articoli \n"
          testo_log = testo_log + " Operazione Teminata  alle " + time.ctime() + "\n"
      #invia e-mail
      type_ = 'plain'
      tools.email_send('Server OpenErp',
                       ['g.dalo@cgsoftware.it'],
                       'Aggiornamento Aliquote iva',
                       testo_log,
                       subtype=type_,
                       )


    
    
var_dati_art()    

